/*
* Grupo 1363
* Pareja 8
* File: move.js
*/

/* Funcion de dragydrop para mover los gatos y el raton en el tablero */
$( function() {
    $( ".canDragDrop" ).draggable({revert: true});
    $( ".image1" ).droppable({
        drop: function( event, ui ) {
            $("input:hidden[name='origin']").val(ui.draggable.attr("id"));
            $("input:hidden[name='target']").val($(this).attr("id"));
            $("#move_form").submit();
        }
    });
  } );
/***********************************************************/
