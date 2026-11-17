"""Tạo Task `batch-review` trên CVAT (Docker, localhost) và nạp pre-label có bẫy. Chỉ dựng Task, KHÔNG duyệt hộ.

    python scripts/cvat_create_review_task.py                     # Task độc lập, nhãn từ cvat/labels_generated.json
    python scripts/cvat_create_review_task.py --project "Day08"   # gắn vào Project Day 08 có sẵn (phải đủ nhãn)

Mật khẩu chỉ nhập qua terminal (getpass) hoặc biến môi trường CVAT_USER / CVAT_PASS; không ghi ra file nào.
"""
import argparse
import getpass
import json
import os
import pathlib
import sys
import time

import requests

ROOT = pathlib.Path(__file__).resolve().parents[1]
LABELS = ROOT / "cvat/labels_generated.json"


def wait_request(s, url, rq_id, what):
    for _ in range(600):
        r = s.get(f"{url}/api/requests/{rq_id}", timeout=30)
        r.raise_for_status()
        st = r.json().get("status")
        if st == "finished":
            print(f"[ OK ] {what}")
            return
        if st == "failed":
            sys.exit(f"[LỖI] {what}: {r.json().get('message')}")
        time.sleep(1)
    sys.exit(f"[LỖI] {what}: quá thời gian chờ")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="http://localhost:8080")
    ap.add_argument("--project", default=None, help="tên Project (mặc định: Project duy nhất có sẵn)")
    ap.add_argument("--name", default="batch-review")
    ap.add_argument("--images", default=str(ROOT / "work/tasks/review"))
    ap.add_argument("--ann", default=str(ROOT / "submission/prelabel/pre_traps_import.coco.json"))
    a = ap.parse_args()

    imgs = sorted(p for p in pathlib.Path(a.images).iterdir() if p.suffix.lower() in (".jpg", ".jpeg", ".png"))
    ann = pathlib.Path(a.ann)
    if len(imgs) != 24:
        sys.exit(f"[LỖI] cần 24 ảnh trong {a.images}, thấy {len(imgs)}: chạy python scripts/prepare_workdirs.py")
    if not ann.exists():
        sys.exit(f"[LỖI] thiếu {ann}: chạy inject_traps.py trước")

    user = os.environ.get("CVAT_USER") or input("CVAT username: ").strip()
    pw = os.environ.get("CVAT_PASS") or getpass.getpass("CVAT password: ")
    s = requests.Session()
    s.auth = (user, pw)

    r = s.get(f"{a.url}/api/users/self", timeout=30)
    if r.status_code != 200:
        sys.exit(f"[LỖI] đăng nhập CVAT thất bại (HTTP {r.status_code}): kiểm tra username / mật khẩu")
    print(f"[ OK ] đăng nhập: {r.json()['username']}")

    body = {"name": a.name}
    if a.project:
        projects = [p for p in s.get(f"{a.url}/api/projects", params={"page_size": 100}, timeout=30).json()["results"]
                    if p["name"] == a.project]
        if len(projects) != 1:
            sys.exit(f"[LỖI] không thấy Project '{a.project}'")
        proj = projects[0]
        labels = {l["name"] for l in s.get(f"{a.url}/api/labels", params={"project_id": proj["id"], "page_size": 100},
                                           timeout=30).json()["results"]}
        need = {l["name"] for l in json.loads(LABELS.read_text(encoding="utf-8"))}
        if not need <= labels:
            sys.exit(f"[LỖI] Project '{proj['name']}' thiếu nhãn {sorted(need - labels)}: không phải Project Day 08")
        body["project_id"] = proj["id"]
        print(f"[ OK ] Project: {proj['name']} (id {proj['id']})")
    else:
        body["labels"] = json.loads(LABELS.read_text(encoding="utf-8"))
        print(f"[ OK ] Task độc lập, nhãn từ {LABELS.relative_to(ROOT)}")

    existing = s.get(f"{a.url}/api/tasks", params={"name": a.name, "page_size": 100}, timeout=30).json()["results"]
    if any(t["name"] == a.name for t in existing):
        sys.exit(f"[LỖI] đã có Task '{a.name}'. Xoá Task đó trên CVAT hoặc dùng --name khác.")

    r = s.post(f"{a.url}/api/tasks", json=body, timeout=30)
    r.raise_for_status()
    tid = r.json()["id"]
    print(f"[ OK ] tạo Task '{a.name}' (id {tid})")

    files = [(f"client_files[{i}]", (p.name, open(p, "rb"), "image/jpeg")) for i, p in enumerate(imgs)]
    data = {"image_quality": 95, "sorting_method": "lexicographical"}
    try:
        r = s.post(f"{a.url}/api/tasks/{tid}/data", data=data, files=files, timeout=600)
    finally:
        for _, (_, fh, _) in files:
            fh.close()
    r.raise_for_status()
    wait_request(s, a.url, r.json()["rq_id"], f"upload {len(imgs)} ảnh")

    with open(ann, "rb") as fh:
        r = s.post(f"{a.url}/api/tasks/{tid}/annotations",
                   params={"format": "COCO 1.0", "location": "local"},
                   files={"annotation_file": (ann.name, fh, "application/json")}, timeout=600)
    r.raise_for_status()
    if r.status_code == 202:
        wait_request(s, a.url, r.json()["rq_id"], f"nạp {ann.name}")

    got = s.get(f"{a.url}/api/tasks/{tid}/annotations", timeout=60).json()["shapes"]
    coco = json.loads(ann.read_text(encoding="utf-8"))
    first = min(coco["images"], key=lambda i: i["file_name"])
    n_first_exp = sum(1 for x in coco["annotations"] if x["image_id"] == first["id"])
    n_first = sum(1 for x in got if x["frame"] == 0)
    ok = len(got) == len(coco["annotations"]) and n_first == n_first_exp
    print(f"[{' OK ' if ok else 'LỖI'}] box trong CVAT: {len(got)} (file: {len(coco['annotations'])}); "
          f"ảnh đầu {first['file_name']}: {n_first} (file: {n_first_exp})")
    print(f"Mở: {a.url}/tasks/{tid}  -> bắt đầu bấm giờ rồi duyệt theo docs/REVIEW_CHECKLIST.md")


if __name__ == "__main__":
    main()
