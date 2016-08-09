<?php

/**
 * Weather Station
 *
 *  PHP version 5
 *
 * @category  weather_station
 * @package   weather_station
 * @author    Mark Roland <mark@markroland.com>
 * @copyright Copyright (c) 2016, Mark Roland
 * @license   http://markroland.com Mark Roland
 * @link      http://markroland.com
 */

/**
 * Set defined constants
 * @param string $resource_path A resource path to a JSON-formatted file (e.g. file://...credentials.json)
 * @return null. Constants
 */
function load_credentials($resource_path)
{
    $json_credentials = '';

    $json_credentials = file_get_contents('file://' . realpath(__DIR__ . '/../../../data/credentials') . '/' . $resource_path);

    if ($json_credentials == false) {
        throw new \Exception('Could not open resource: ' . $resource_path);
    }

    $credentials = json_decode($json_credentials);

    if (is_null($credentials)) {
        throw new \Exception('JSON credentials could not be decoded from resource: ' . $resource_path);
    }

    return $credentials;
}

// Connect to database using PDO
$pdo_connection = null;
$mysql_credentials = load_credentials('mysql_mark.json');
try {
    $pdo_connection = new PDO(
        'mysql:host=localhost;dbname=markr34_weather_station;charset=utf8',
        $mysql_credentials->DB_USERNAME,
        $mysql_credentials->DB_PASSWORD
    );
    $pdo_connection->setAttribute(\PDO::ATTR_ERRMODE, \PDO::ERRMODE_EXCEPTION);
    $pdo_connection->setAttribute(\PDO::ATTR_DEFAULT_FETCH_MODE, \PDO::FETCH_ASSOC);
} catch (PDOException $e) {
    error_log('ERROR: ' . $e->getMessage() . "\n");
}

// Handle request
if (preg_match('@^/weather-station/([0-9]+)?$@i', $_SERVER['REQUEST_URI'])) {

    if ($_SERVER['REQUEST_METHOD'] == 'GET') {

        $template = 'file://' . realpath(__DIR__) . '/graph.html';

        print(file_get_contents($template));
        exit;

    }

    elseif ($_SERVER['REQUEST_METHOD'] == 'POST') {

        // Parse input
        $POST_data = json_decode(file_get_contents("php://input"));

        // Build database object
        $data = [
            'station_id' => $POST_data->station_id,
            'log_time' => $POST_data->log_time,
            'temperature' => $POST_data->temperature,
            'humidity' => $POST_data->humidity,
            'pressure' => $POST_data->pressure,
            'light' => isset($POST_data->light) ? $POST_data->light : null,
            'wind' => isset($POST_data->wind) ? $POST_data->wind : null,
            'rain' => isset($POST_data->rain) ? $POST_data->rain : null
        ];

        // Insert into database
        try {
            $query = $pdo_connection->prepare(
                "INSERT INTO `markr34_weather_station`.`station_log`
                SET station_id = ?,
                log_time = ?,
                temperature = ?,
                humidity = ?,
                pressure =?,
                light = ?,
                wind = ?,
                rain = ?"
            );
            $query->execute(array_values($data));
        } catch (\PDOException $e) {

        }

    }

    header('Content-Type: application/json; charset=utf-8');
    print(json_encode($data));
    exit;
}

if (preg_match('@^/weather-station/1/data\.json$@i', $_SERVER['REQUEST_URI'])) {

    if ($_SERVER['REQUEST_METHOD'] == 'GET') {
        try {
            $query = $pdo_connection->prepare(
                "SELECT * FROM  `markr34_weather_station`.`station_log` WHERE station_id = 1"
            );
            $query->execute();
            $data = $query->fetchAll();
        } catch (\PDOException $e) {

        }

        header('Content-Type: application/json');
        print(json_encode($data));
        exit;
    }
}