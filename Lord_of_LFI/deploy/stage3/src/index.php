<?php
if ($_GET['file']) {
    $file = basename($_GET['file']);

    if (file_exists($file)) {
        include($file.'php');
    }

    include($file);
}
?>
