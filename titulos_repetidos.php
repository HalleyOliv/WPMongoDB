<?php
/**
 * @file
 * Exibir os títulos repetidos dos documentos,
 * ordenados pelo número de vezes que aparecem
 * e título.
 *
 * @author Halley Pacheco de Oliveira
 */

// Estabelecer a conexão com o MongoDB
$conn = new MongoDB\Driver\Manager("mongodb://localhost:27017");

// Utilizar a agregação para contar o número de vezes
// que cada título aparece na coleção.
// _id é o campo usado para agrupar a coleção.
// Mostrar só os títulos repetidos, ou seja,
// aqueles que aparecem mais de uma vez.
$comando = new MongoDB\Driver\Command( [
    'aggregate' => 'pages',
    'pipeline' => [
        [ '$group' => [ '_id' => '$title', 'contador' => ['$sum' => 1] ] ],
        [ '$match' => [ 'contador' => [ '$gt' => 1 ] ] ],
        [ '$sort'  => [ 'contador' => 1, '_id' => 1] ],
    ],
    'cursor' => new stdClass,
] );

// Executar o comando criando um cursor para o resultado
$cursor = $conn->executeCommand('reficio', $comando);

// Mostrar o resultado
foreach ($cursor as $documento) {
    $doc = get_object_vars($documento);
    echo $doc["_id"] . "; " . $doc["contador"] . "<br />";
}
?>
