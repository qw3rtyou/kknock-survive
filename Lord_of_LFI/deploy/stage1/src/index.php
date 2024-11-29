<?php
if ($_GET['file']) {
    $file = basename($_GET['file']);

    include($file);
}
?>
