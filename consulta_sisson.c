/*
 * @file
 * Exibe os documentos cujo título é 
 * Sébastien Auguste Sisson (apenas um).
 *
 * Baseado no exemplo mostrado em
 * http://mongoc.org/libmongoc/current/tutorial.html
 *
 * @author Halley Pacheco de Oliveira
 */

#include < bson.h > #include < mongoc.h > #include < stdio.h >

  int main(int argc, char * argv[]) {
    mongoc_client_t * cliente;
    mongoc_collection_t * colecao;
    mongoc_cursor_t * cursor;
    const bson_t * doc;
    bson_t * consulta;
    char * str;
    bson_iter_t iterator;
    uint32_t * length;

    mongoc_init();

    cliente = mongoc_client_new("mongodb://localhost:27017/?appname=consulta-sisson");
    colecao = mongoc_client_get_collection(cliente, "reficio", "pages");
    consulta = bson_new();
    BSON_APPEND_UTF8(consulta, "title", "Sébastien Auguste Sisson");
    cursor = mongoc_collection_find_with_opts(colecao, consulta, NULL, NULL);

    while (mongoc_cursor_next(cursor, & doc)) {
      if (bson_iter_init_find( & iterator, doc, "title")) {
        printf("Título: %s\n", bson_iter_utf8( & iterator, length));
      }
      if (bson_iter_init_find( & iterator, doc, "excerpt")) {
        printf("Sumário: %s\n", bson_iter_utf8( & iterator, length));
      }
    }

    bson_destroy(consulta);
    mongoc_cursor_destroy(cursor);
    mongoc_collection_destroy(colecao);
    mongoc_client_destroy(cliente);
    mongoc_cleanup();

    return 0;
  }