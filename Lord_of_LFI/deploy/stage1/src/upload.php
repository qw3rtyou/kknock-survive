<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_FILES['file'])) {
        $fileName = basename($_FILES['file']['name']);
        $fileExtension = pathinfo($fileName, PATHINFO_EXTENSION);

        $blockedExtensions = '/phtml|phar|pht|htm|html|hta/i';
        if (preg_match($blockedExtensions, $fileExtension)) {
            echo "This file type is not allowed.";
            exit;
        }

        if (move_uploaded_file($_FILES['file']['tmp_name'], $fileName)) {
            echo "File uploaded successfully: <a href='$fileName'>$fileName</a>";
        } else {
            echo "Failed to upload file.";
        }
    } else {
        echo "No file uploaded.";
    }
}
?>

<form method="post" enctype="multipart/form-data">
    <input type="file" name="file" required>
    <button type="submit">Upload</button>
</form>
