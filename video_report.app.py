import os
import csv
import io
from flask import Flask, render_template, send_file, abort, Response, request

app = Flask(__name__)

VIDEO_DIR = os.path.join(os.path.dirname(__file__), 'videos')

@app.route("/")
def report():
    try:
        videos = [f for f in os.listdir(VIDEO_DIR) if os.path.isfile(os.path.join(VIDEO_DIR, f))]
    except Exception as e:
        videos = []
    video_data = [
        {
            "name": fname,
            "link": f"/video/{fname}"
        }
        for fname in videos
    ]
    return render_template("report.html", video_data=video_data)

@app.route("/download_csv")
def download_csv():
    try:
        videos = [f for f in os.listdir(VIDEO_DIR) if os.path.isfile(os.path.join(VIDEO_DIR, f))]
    except Exception as e:
        videos = []
    # Build CSV content in-memory
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['File Name', 'Links'])
    for fname in videos:
        link = f"{request.host_url}video/{fname}"
        writer.writerow([fname, link])
    csv_content = output.getvalue()
    output.close()
    return Response(
        csv_content,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=video_report.csv"}
    )

@app.route("/video/<filename>")
def video(filename):
    file_path = os.path.join(VIDEO_DIR, filename)
    if not os.path.exists(file_path):
        abort(404)
    return send_file(file_path, as_attachment=False)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
