function print_mail_IA(){
    const div_IA = document.querySelector("#div_IA");
    const div_manual = document.querySelector("#div_manual");

    div_IA.style = "display : none";
    div_manual.style = "display: flex; flex-direction: column;";
}

function print_mail_manual(){
    const div_IA = document.querySelector("#div_manual");
    const div_manual = document.querySelector("#div_IA");

    div_IA.style = "display : none";
    div_manual.style = "display: flex; flex-direction: column;";
}

function send_mail_IA(){
    const div_IA = document.querySelector("#send_IA");
    const div_manual = document.querySelector("#send_manual");

    div_IA.style = "display : none";
    div_manual.style = "display: flex; flex-direction: column;";
}

function send_mail_manual(){
    const div_IA = document.querySelector("#send_IA");
    const div_manual = document.querySelector("#send_manual");

    div_IA.style = "display: flex; flex-direction: column;";
    div_manual.style = "display : none";
}