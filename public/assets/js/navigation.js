$(document).ready(function (e) {
  var n = e(".js-subnav-trigger");
  n.click(function (t) {
    t.preventDefault();
    var n = e(this).find(".nav-subnav-action"),
      i = n.parent().parent().children(".nav-subnav");
    n.parent();
    return i.hasClass("nav-subnav-isopen")
      ? (i.removeClass("nav-subnav-isopen"), void n.html("+"))
      : (e(".nav-subnav").removeClass("nav-subnav-isopen"),
        e(".nav-subnav-action").html("+"),
        i.addClass("nav-subnav-isopen"),
        n.html("-"),
        !1);
  });
  var i = e(".nav-icon"),
    r = e(".nav");
  i.click(function () {
    "none" === r.css("display")
      ? (r.addClass("show"),
        i.removeClass("closed").addClass("open"),
        i.children(".las").removeClass("la-bars").addClass("la-times"))
      : (r.removeClass("show"),
        i.removeClass("open").addClass("closed"),
        i.children(".las").removeClass("la-times").addClass("la-bars"));
  });
});
