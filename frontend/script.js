async function upload() {

    let file = document.getElementById("fileInput").files[0];

    let formData = new FormData();
    formData.append("file", file);

    let res = await fetch("http://127.0.0.1:8000/upload", {
        method: "POST",
        body: formData
    });

    let blob = await res.blob();
    let url = window.URL.createObjectURL(blob);

    let a = document.createElement("a");
    a.href = url;
    a.download = "Final_CBSE_Result.xlsx";
    a.click();
}
