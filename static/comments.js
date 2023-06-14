$( document ).ready(function() {
    $(".cmt_btn").click(function () {

      formId = $(this).attr("class").split(/\s+/)[1]

      $(`.form${formId}`)[0][2].focus()
    });
})
