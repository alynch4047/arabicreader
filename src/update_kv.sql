UPDATE kalima_variation
   SET kalvar_number=(select kalima_number from kalima
        where kalima.kalima_id = kalima_variation.kalima_id) ;

UPDATE kalima_variation
   SET kalvar_text=(select kalima_text from kalima
        where kalima.kalima_id = kalima_variation.kalima_id) ;

UPDATE kalima_variation
   SET kalvar_meaning=(select kalima_meaning from kalima
        where kalima.kalima_id = kalima_variation.kalima_id) ;

UPDATE kalima_variation
   SET kalvar_tense=(select kalima_tense from kalima
        where kalima.kalima_id = kalima_variation.kalima_id) ;

UPDATE kalima_variation
   SET kalvar_type=(select kalima_type from kalima
        where kalima.kalima_id = kalima_variation.kalima_id) ;
