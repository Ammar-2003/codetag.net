var script = document.createElement("script");
script.type = "text/javascript";
script.src =
  "https://cdn.tiny.cloud/1/nv6yonelsgckys945wprnzhqi4ndd0v8vsl9d19mlt7xy7pj/tinymce/7/tinymce.min.js";
document.head.appendChild(script);

script.onload = function () {
  tinymce.init({
    selector: "#id_content",
    plugins: [
      "anchor",
      "autolink",
      "charmap",
      "codesample",
      "emoticons",
      "image",
      "link",
      "lists",
      "media",
      "searchreplace",
      "table",
      "visualblocks",
      "wordcount",
      "checklist",
      "mediaembed",
      "casechange",
      "formatpainter",
      "pageembed",
      "a11ychecker",
      "tinymcespellchecker",
      "permanentpen",
      "powerpaste",
      "advtable",
      "advcode",
      "editimage",
      "advtemplate",
      "ai",
      "mentions",
      "tinycomments",
      "tableofcontents",
      "footnotes",
      "mergetags",
      "autocorrect",
      "typography",
      "inlinecss",
      "markdown",
      "importword",
      "exportword",
      "exportpdf",
    ],
    toolbar:
      "undo redo | styles | bold italic | alignleft aligncenter alignright alignjustify | " +
      "bullist numlist outdent indent | link image | print preview media fullscreen | " +
      "forecolor backcolor emoticons | help",
    menu: {
      favs: {
        title: "My Favorites",
        items: "code visualaid | searchreplace | emoticons",
      },
    },
    menubar: "favs file edit view insert format tools table help",
    content_css: "/static/css/tinymce-content.css", // Path to your new CSS file
    body_class: "article-container", // Match frontend container class
    height: 600,
    branding: false,
  });
};
