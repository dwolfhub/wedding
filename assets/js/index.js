

(function () {
    /* TABS */
    var sections = document.querySelectorAll('section');
    var sectionButtons = document.querySelectorAll('.menu a');
    var tabButtonClicked = function (event) {
        event.preventDefault();

        for (var i = 0; i < sectionButtons.length; i++) {
            sectionButtons[i].classList.remove('active');
        }
        this.classList.add('active');

        for (var i = 0; i < sections.length; i++) {
            sections[i].classList.remove('active');
        }

        var selector = '#section-' + this.href.split('#').pop();
        document.querySelector(selector).classList.add('active');
    };

    for (var i = 0; i < sectionButtons.length; i++) {
        sectionButtons[i].addEventListener('click', tabButtonClicked);
    }
})();
