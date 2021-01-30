/*
* Grupo 1363
* Pareja 8
* File: reproduccion.js
*/

var idvar; /* Variable del setInterval */

/* CONTROL DEL CSRF TOKEN PARA LAS PETICIONES POST DE AJAX */
$(document).ready(function(){
    function getCookie(c_name) {
        if(document.cookie.length > 0) {
            c_start = document.cookie.indexOf(c_name + "=");
            if(c_start != -1) {
                c_start = c_start + c_name.length + 1;
                c_end = document.cookie.indexOf(";", c_start);
                if(c_end == -1) c_end = document.cookie.length;
                return unescape(document.cookie.substring(c_start,c_end));
            }
        }
        return "";
    }

    $(function () {
        $.ajaxSetup({
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            }
        });
    });
});
/***********************************************************/

/* Funcion de play. Se ejecuta cada 2 segundos. */
function play() {            
    $.ajax({
        url:'/logic/get_move/',
        type: 'post',
        data: {"shift":1},
        success: function(response) {
            var idOrigin = "#" + response['origin'];
            var idTarget = "#" + response['target'];
            image1 = $(idOrigin + " + .image2").attr("src");
            image2 = $(idTarget + " + .image2").attr("src");
            $(idOrigin + " + .image2").attr("src", image2);
            $(idTarget + " + .image2").attr("src", image1);
            if(response['next'] == false){
                $("#winImage").removeClass("hidden");
                window.clearInterval(idvar);
            }
        }, 
    });
}
/***********************************************************/

/* Funciones de next, previous, play y stop */
$( function() {

    /* Funcion de siguiente movimiento a mostrar por pantalla */
    $('#next').click(function(){
        $.ajax({
            url:'/logic/get_move/',
            type: 'post',
            data: {"shift":1},
            success: function(response) {
                var idOrigin = "#" + response['origin'];
                var idTarget = "#" + response['target'];
                image1 = $(idOrigin + " + .image2").attr("src");
                image2 = $(idTarget + " + .image2").attr("src");
                $(idOrigin + " + .image2").attr("src", image2);
                $(idTarget + " + .image2").attr("src", image1);
                if(response['next'] == false){
                    $("#winImage").removeClass("hidden");
                }
            }, 
        });
    });

    /* Funcion de anterior movimiento a mostrar por pantalla */
    $('#previous').click(function(){
        $.ajax({
            url:'/logic/get_move/',
            type:'post',
            data: {"shift":-1},
            success: function(response) {
                var idOrigin = "#" + response['origin'];
                var idTarget = "#" + response['target'];
                image1 = $(idOrigin + " + .image2").attr("src");
                image2 = $(idTarget + " + .image2").attr("src");
                $(idOrigin + " + .image2").attr("src", image2);
                $(idTarget + " + .image2").attr("src", image1);
                if(response['next'] == true){
                    $("#winImage").addClass("hidden");
                }
            },
        });
    });

    /* Funcion de mostrar por pantalla todos los movimientos en orden */
    $('#play').click(() => {
        idvar = setInterval("play()", 2000, true);
    });

    /* Funcion de parar la reproduccion anterior */
    $('#stop').click(function(){
        window.clearInterval(idvar);
    });
});
/***********************************************************/
