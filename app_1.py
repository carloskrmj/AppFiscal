
import openai


def gerar_resposta(pergunta):
    # Initialize the API key
    #openai.api_key = "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"
    openai.api_key = "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"
    messages = [{"role": "user", "content": pergunta}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1024,
        temperature=0.5
    )
    return [response.choices[0].message.content, response.usage]


#mensagens = [{"role": "user", "content": "Você conhece o Mário?"}]
#resposta = gerar_resposta(mensagens)[0]
#print(resposta)
"""while True:
    # Ask a question
    question = input("Perguntar pro ChatGPT (\"sair\"): ")

    if question == "sair" or question == "":
        print("saindo")
        break
    else:
        mensagens.append({"role": "user", "content": str(question)})

        answer = gerar_resposta(mensagens)
        print("Nóis:", question)
        print("ChatGPT:", answer[0], "\nCusto:\n", answer[1])
        mensagens.append({"role": "assistant", "content": answer[0]})

    debugar = False
    if debugar:
        print("Mensagens", mensagens, type(mensagens))"""