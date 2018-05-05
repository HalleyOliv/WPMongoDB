<?php
/**
 * @file
 * Gera o arquivo a ser importado pelo MongoDB
 * a partir das páginas do WordPress.
 *
 * Este script é colocado no diretório raiz do
 * WordPress, enquanto o arquivo de saída é
 * escrito no diretório do tema ativo.
 *
 * Este script é baseado no script desenvolvido
 * por Gabriele Romanato mostrado na página:
 * How to export data from WordPress to MongoDB
 * https://gabrieleromanato.name/how-to-export-data-from-wordpress-to-mongodb
 */
require_once( 'wp-load.php' );
get_header();
$export_file = 'reficio.json';
$loop        = new WP_Query( array(
    'post_type' => 'page',
    'posts_per_page' => -1 
) );
$data        = array();
while ( $loop->have_posts() ):
    $loop->the_post();
    $id              = get_the_ID();
    $upload_dir      = wp_upload_dir();
    $base_upload_url = $upload_dir['baseurl'] . '/';
    $thumb           = wp_get_attachment_image_src( get_post_thumbnail_id( $id ), 'full' );
    $image           = str_replace( $base_upload_url, '/uploads/', $thumb[0] );
    $ancestors       = get_ancestors( $id, 'page', 'post_type' );

    $coordinates = array();

    $coord_values = get_post_custom_values( 'Coordenadas', $id );
    foreach ( $coord_values as $key => $value ) {
        $latlon        = explode( ",", $value );
        $lat           = (double) filter_var( $latlon[0], FILTER_SANITIZE_NUMBER_FLOAT, FILTER_FLAG_ALLOW_FRACTION );
        $lon           = (double) filter_var( $latlon[1], FILTER_SANITIZE_NUMBER_FLOAT, FILTER_FLAG_ALLOW_FRACTION );
        $coordinates[] = array(
            $lon,
            $lat 
        );
    }
    $datum                = array();
    $datum['id']          = $id;
    $datum['title']       = get_the_title();
    $datum['date']        = new \MongoDB\BSON\UTCDateTime(strtotime(get_the_date( 'Y-m-d\TH:i:s\Z', $id )));
    $datum['content']     = get_the_content();
    $datum['excerpt']     = strip_tags( get_the_excerpt() );
    $datum['slug']        = basename( get_permalink( $id ) );
    $datum['thumb']       = $image;
    $datum['ancestors']   = $ancestors;
    $datum['coordinates'] = $coordinates;
    $data[]               = $datum;
endwhile;
wp_reset_postdata();

$json = json_encode( $data );
file_put_contents( TEMPLATEPATH . '/' . $export_file, $json );
get_footer();
?>
