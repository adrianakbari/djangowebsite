/*global $, document, Chart, LINECHART, data, options, window, setTimeout*/
$(document).ready(function () {

    'use strict';

    // smooth scroll of the contact link
    $('a#contact').click(function () {
        $("html, body").animate(
            {
                scrollTop: $(document).height(),
            },
            1000,
            "easeInOutExpo"
        );
        return false;
    });
    // smooth scroll of the scroll down link
    $('a.continue.link-scroll[href*="#"]:not([href="#"])').click(function () {
        if (
            location.pathname.replace(/^\//, "") ==
            this.pathname.replace(/^\//, "") &&
            location.hostname == this.hostname
        ) {
            var target = $(this.hash);
            target = target.length
                ? target
                : $("[name=" + this.hash.slice(1) + "]");
            if (target.length) {
                $("html, body").animate(
                    {
                        scrollTop: target.offset().top - 70,
                    },
                    1000,
                    "easeInOutExpo"
                );
                return false;
            }
        }
    });


    // ------------------------------------------------------- //
    // For demo purposes only
    // ------------------------------------------------------ //

    var stylesheet = $('link#theme-stylesheet');
    $("<link id='new-stylesheet' rel='stylesheet'>").insertAfter(stylesheet);
    var alternateColour = $('link#new-stylesheet');

    if ($.cookie("theme_csspath")) {
        alternateColour.attr("href", $.cookie("theme_csspath"));
    }

    $("#colour").change(function () {

        if ($(this).val() !== '') {

            var theme_csspath = 'css/style.' + $(this).val() + '.css';

            alternateColour.attr("href", theme_csspath);

            $.cookie("theme_csspath", theme_csspath, { expires: 365, path: document.URL.substr(0, document.URL.lastIndexOf('/')) });

        }

        return false;
    });


    // ------------------------------------------------------- //
    // Equalixe height
    // ------------------------------------------------------ //
    function equalizeHeight(x, y) {
        var textHeight = $(x).height();
        $(y).css('min-height', textHeight);
    }
    equalizeHeight('.featured-posts .text', '.featured-posts .image');

    $(window).resize(function () {
        equalizeHeight('.featured-posts .text', '.featured-posts .image');
    });


    // ---------------------------------------------- //
    // Preventing URL update on navigation link click
    // ---------------------------------------------- //
    $('.link-scroll').bind('click', function (e) {
        var anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $(anchor.attr('href')).offset().top + 2
        }, 700);
        e.preventDefault();
    });


    // ---------------------------------------------- //
    // FancyBox
    // ---------------------------------------------- //
    $("[data-fancybox]").fancybox();


    // ---------------------------------------------- //
    // Divider Section Parallax Background
    // ---------------------------------------------- //
    $(window).on('scroll', function () {

        var scroll = $(this).scrollTop();

        if ($(window).width() > 1250) {
            $('section.divider').css({
                'background-position': 'left -' + scroll / 8 + 'px'
            });
        } else {
            $('section.divider').css({
                'background-position': 'center bottom'
            });
        }
    });


    // ---------------------------------------------- //
    // Search Bar
    // ---------------------------------------------- //
    $('.search-btn').on('click', function (e) {
        e.preventDefault();
        $('.search-area').fadeIn();
    });
    $('.search-area .close-btn').on('click', function () {
        $('.search-area').fadeOut();
    });



    // ---------------------------------------------- //
    // Navbar Toggle Button
    // ---------------------------------------------- //
    // $('.navbar-toggler').on('click', function () {
    //     $('.navbar-toggler').toggleClass('active');
    // });

    $('.nav-link.header').each(function () {
        if (
            location.pathname.replace(/^\//, "") ==
            this.pathname.replace(/^\//, "") &&
            location.hostname == this.hostname
        ) {
            $(".nav-link.header").find(".active").removeClass("active");
            $(this).addClass("active");
        }
    })
    // ------------------------------------------------------- //
    // My test
    // ------------------------------------------------------ //
    // $("#popup").mouseover(function () {
    //     console.log("mouseover");
    // });
    // ------------------------------------------------------- //
    // Resume projcts tooltips
    // ------------------------------------------------------ //
    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    })
    // ------------------------------------------------------- //
    // Certificate venobox
    // ------------------------------------------------------ //
    $('.venobox').venobox({
        'share': false
    });
    // tiny mce is designed with django-tinymce DO NOT combine it with normal tinymce
    // ------------------------------------------------------- //
    // TinyCME Bug Removal
    // TinyMCE-Django has a bug that cant be applied when there are 2 editors on the same page. the script here under fixs it.
    // ------------------------------------------------------ //
    // function tinymce4_init(selector) {
    //     var tinymce4_config = { setup: function (editor) { editor.on('change', function () { editor.save(); }); }, "language": "en", "directionality": "ltr", "cleanup_on_startup": true, "custom_undo_redo_levels": 20, "selector": "textarea.tinymce4-editor", "theme": "modern", "plugins": "\n            textcolor save link image media preview codesample contextmenu\n            table code lists fullscreen  insertdatetime  nonbreaking\n            contextmenu directionality searchreplace wordcount visualblocks\n            visualchars code fullscreen autolink lists  charmap print  hr\n            anchor pagebreak\n            ", "toolbar1": "\n            fullscreen preview bold italic underline | fontselect,\n            fontsizeselect  | forecolor backcolor | alignleft alignright |\n            aligncenter alignjustify | indent outdent | bullist numlist table |\n            | link image media | codesample |\n            ", "toolbar2": "\n            visualblocks visualchars |\n            charmap hr pagebreak nonbreaking anchor |  code |\n            ", "contextmenu": "formats | link image", "menubar": true, "statusbar": true }; if (typeof selector != 'undefined') { tinymce4_config['selector'] = selector; }
    //     tinymce.init(tinymce4_config);

    // }
    // tinymce4_init();

    // tinymce.init({
    //     selector: 'textarea.tinymcewidget'
    // });

});