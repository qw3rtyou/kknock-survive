import os
import tempfile
import tarfile
import zipfile
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from auth import login_required
import subprocess

audit_bp = Blueprint("audit_bp", __name__)

UPLOAD_FOLDER = "/tmp"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
SECRETCODE = os.environ.get("SECRETCODE", "default_secret_code")


@audit_bp.route("/audit", methods=["GET", "POST"])
@login_required
def audit():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)

        files = request.files.getlist("file")

        if not files or all(file.filename == "" for file in files):
            flash("No selected file(s)")
            return redirect(request.url)

        temp_dir = tempfile.mkdtemp(dir=UPLOAD_FOLDER)

        if len(files) == 1:
            file = files[0]
            if archived_file(file.filename):
                file_path = os.path.join(temp_dir, file.filename)
                file.save(file_path)

                extract_archive(file_path, temp_dir)
                raw_tree_output = subprocess.check_output(
                    ["tree", "-fi", temp_dir], universal_newlines=True
                )
                tree_output_html = generate_tree_html(
                    raw_tree_output.splitlines(), temp_dir
                )

                session["temp_dir"] = temp_dir
                return render_template("audit/tree.html", tree_output=tree_output_html)

        else:
            for file in files:
                file_path = os.path.join(temp_dir, file.filename)
                file.save(file_path)

            cookie_value = request.cookies.get("SECRETCODE")

            if cookie_value == SECRETCODE:
                try:
                    tar_file_path = os.path.join(temp_dir, "tmp.tar.gz")
                    subprocess.run(
                        f"tar -czf tmp.tar.gz *", shell=True, cwd=temp_dir, check=True
                    )
                except subprocess.CalledProcessError as e:
                    flash(f"Error occurred during tar creation: {e}")
                    return redirect(request.url)

                extract_archive(tar_file_path, temp_dir)

            raw_tree_output = subprocess.check_output(
                ["tree", "-fi", temp_dir], universal_newlines=True
            )
            tree_output_html = generate_tree_html(
                raw_tree_output.splitlines(), temp_dir
            )

            session["temp_dir"] = temp_dir
            return render_template("audit/tree.html", tree_output=tree_output_html)

    return render_template("audit/upload.html")


@audit_bp.route("/tree", methods=["GET"])
@login_required
def tree_view():
    temp_dir = session.get("temp_dir")

    if not temp_dir or not os.path.exists(temp_dir):
        flash("The project directory is no longer available.")
        return redirect(url_for("audit_bp.audit"))

    raw_tree_output = subprocess.check_output(
        ["tree", "-fi", temp_dir], universal_newlines=True
    )

    tree_output_html = generate_tree_html(raw_tree_output.splitlines(), temp_dir)

    return render_template("audit/tree.html", tree_output=tree_output_html)


def archived_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {
        "tar",
        "gz",
        "zip",
    }


def extract_archive(filepath, extract_to):
    if filepath.endswith("tar.gz") or filepath.endswith("tgz"):
        with tarfile.open(filepath, "r:gz") as tar:
            tar.extractall(path=extract_to)
    elif filepath.endswith(".zip"):
        with zipfile.ZipFile(filepath, "r") as zip_ref:
            zip_ref.extractall(path=extract_to)
    elif filepath.endswith(".tar"):
        with tarfile.open(filepath, "r:") as tar:
            tar.extractall(path=extract_to)


def generate_tree_html(tree_lines, base_dir):
    html_output = ""
    for line in tree_lines:
        file_or_dir = line.strip()

        file_path = file_or_dir

        if os.path.isfile(file_path):
            html_output += f'<a href="#" class="file-link" data-file-path="{file_path}">{file_or_dir[16:]}</a><br>'

    return html_output.strip()
