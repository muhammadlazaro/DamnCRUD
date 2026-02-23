<?php

function pdo_connect(){
    $DATABASE_HOST = getenv('DB_HOST') ?: '127.0.0.1';
    $DATABASE_USER = getenv('DB_USER') ?: 'root';
    $DATABASE_PASS = getenv('DB_PASS') ?: '';
    $DATABASE_NAME = getenv('DB_NAME') ?: 'damncrud';

    try {
        return new PDO(
            'mysql:host=' . $DATABASE_HOST . ';dbname=' . $DATABASE_NAME . ';charset=utf8',
            $DATABASE_USER,
            $DATABASE_PASS,
            [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]
        );
    } catch (PDOException $exception) {
        die('Failed to connect to database: ' . $exception->getMessage());
    }
}

function style_script(){
    return '
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdn.datatables.net/1.10.20/css/dataTables.bootstrap4.min.css">
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/js/bootstrap.bundle.min.js"></script>   
    <script src="https://cdn.datatables.net/1.10.20/js/jquery.dataTables.min.js"></script>
    <script src="https://cdn.datatables.net/1.10.20/js/dataTables.bootstrap4.min.js"></script>';
}
