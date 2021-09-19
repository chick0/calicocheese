function btn_init(project_id){
    axios({
        method:"GET",
        url: "/api/link",
        params: {
            id: project_id
        }
    }).then(function(response){
        response.data.forEach(function(link){
            let color   = link.color;
            let text    = link.text;
            let url     = link.url;
            let display = document.getElementById("link-button");
            let button  = document.createElement("a");

            button.setAttribute("class", "btn " + color);
            button.setAttribute("href", url);
            button.setAttribute("target", "_blank");
            button.setAttribute("rel", "no" + "referrer");
            button.innerText = text;

            display.appendChild(button);
            display.appendChild(document.createTextNode(" "));
        });
    });
}
