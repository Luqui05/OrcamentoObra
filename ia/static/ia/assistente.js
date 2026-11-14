const formulario = document.querySelector("#ia-pergunta-form");
const campoPergunta = formulario.elements.pergunta;
const botaoEnviar = formulario.querySelector('button[type="submit"]');
const csrf = formulario.elements.csrfmiddlewaretoken.value;
const statusEnvio = document.querySelector("#ia-status");
const erroEnvio = document.querySelector("#ia-erro");
const historico = document.querySelector("#ia-interacoes");
const modeloInteracao = document.querySelector("#ia-interacao-template");

formulario.addEventListener("submit", async (evento) => {
    evento.preventDefault();
    if (botaoEnviar.disabled) {
        return;
    }

    const dados = new FormData(formulario);
    botaoEnviar.disabled = true;
    campoPergunta.readOnly = true;
    erroEnvio.hidden = true;
    statusEnvio.hidden = false;
    statusEnvio.textContent = "Aguardando resposta do assistente…";

    try {
        const resposta = await fetch(formulario.action, {
            method: "POST",
            credentials: "same-origin",
            headers: { "X-CSRFToken": csrf, Accept: "application/json" },
            body: dados,
        });
        const tipo = resposta.headers.get("Content-Type") ?? "";
        if (!tipo.includes("application/json")) {
            const mensagem = resposta.status === 403
                ? "Atualize a página e tente novamente."
                : "Não foi possível enviar a pergunta.";
            throw new Error(mensagem);
        }

        const resultado = await resposta.json();
        if (!resposta.ok) {
            throw new Error(resultado.erro || "Não foi possível enviar a pergunta.");
        }

        const interacao = modeloInteracao.content.cloneNode(true);
        interacao.querySelector(".ia-pergunta").textContent = resultado.pergunta;
        // O servidor renderiza o Markdown sem HTML cru, imagens ou URLs perigosas.
        interacao.querySelector(".ia-resposta").innerHTML = resultado.resposta_html;
        document.querySelector("#ia-sem-interacoes")?.remove();
        historico.prepend(interacao);
        formulario.reset();
        statusEnvio.textContent = "Resposta recebida. Consulte o histórico.";
    } catch (erro) {
        statusEnvio.hidden = true;
        erroEnvio.hidden = false;
        erroEnvio.textContent = erro.message;
    } finally {
        botaoEnviar.disabled = false;
        campoPergunta.readOnly = false;
        campoPergunta.focus();
    }
});
