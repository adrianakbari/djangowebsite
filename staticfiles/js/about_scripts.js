/*!
    * Start Bootstrap - Grayscale v6.0.3 (https://startbootstrap.com/theme/grayscale)
    * Copyright 2013-2020 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-grayscale/blob/master/LICENSE)
    */
(function ($) {
    "use strict"; // Start of use strict


    // Smooth scrolling using jQuery easing
    $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function () {
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

    // Closes responsive menu when a scroll trigger link is clicked
    $(".js-scroll-trigger").click(function () {
        $(".navbar-collapse").collapse("hide");
    });

    // Activate scrollspy to add active class to navbar items on scroll
    $("body").scrollspy({
        target: "#mainNav",
        offset: 100,
    });
    // jQuery counterUp
    $('[data-toggle="counter-up"]').counterUp({
        delay: 10,
        time: 1000
    });

    //tiny slider
    if ($('.my-slider').length) {
        var slider = tns({
            container: '.my-slider',
            items: 5,
            slideBy: 1,
            mouseDrag: true,
            swipeAngle: false,
            speed: 200,
            controls: false,
            navPosition: 'bottom',
            autoplay: true,
            autoplayHoverPause: true,
            autoplayTimeout: 3500,
            preventActionWhenRunning: true,
            autoplayText: [
                "",
                ""
            ],
            responsive: {
                350: {
                    edgePadding: 30,
                    gutter: 0,
                    items: 1,
                    controls: false,
                    center: true,
                    autoplayHoverPause: true,
                },
                640: {
                    edgePadding: 20,
                    gutter: 0,
                    items: 2,
                    center: true,
                    autoplayHoverPause: true,
                },
                900: {
                    items: 3
                }
            }
        });
    }
    // Init AOS
    function aos_init() {
        AOS.init({
            duration: 1000,
            easing: "ease-in-out-back",
            once: true
        });
    }
    $(window).on('load', function () {
        aos_init();
    });

    // // Collapse Navbar
    // var navbarCollapse = function () {
    //     if ($("#mainNav").offset().top > 100) {
    //         $("#mainNav").addClass("navbar-shrink");
    //     } else {
    //         $("#mainNav").removeClass("navbar-shrink");
    //     }
    // };
    // // Collapse now if page is not at top
    // navbarCollapse();
    // // Collapse the navbar when page is scrolled
    // $(window).scroll(navbarCollapse);
})(jQuery); // End of use strict
