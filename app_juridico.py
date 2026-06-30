import streamlit as str
import google.generativeai as genai
import os
import time

# Configuração da página para o celular
str.set_page_config(page_title="Degravação Jurídica", page_icon="⚖️", layout="centered")

str.title("⚖️ Assistente de Degravação Forense")
str.write("Grave ou envie o áudio de suas audiências, reuniões ou ditados para transcrição jurídica formal.")

# Configuração da API do Gemini
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    str.error("Chave de API do Gemini não configurada.")

# Interface de Upload (Agora suportando explicitamente mp4)
arquivo_audio = str.file_uploader("📂 Selecione o áudio ou vídeo do seu celular:", type=["mp4", "mp3", "wav", "m4a", "aac", "ogg"])

# Opções de formatação jurídica
opcao_formato = str.selectbox(
    "📝 Escolha o tom/formatação do documento:",
    [
        "Transcrição Ipsis Litteris (Exata, ideal para depoimentos e provas)",
        "Ditado de Peça Processual (Formatação formal em tópicos/parágrafos)",
        "Resumo de Audiência/Reunião (Pontos principais e deliberações)"
    ]
)

botao_processar = str.button("✨ Iniciar Degravação Jurídica", use_container_width=True)

if botao_processar:
    if arquivo_audio is not None:
        try:
            nome_arquivo = arquivo_audio.name
            with open(nome_arquivo, "wb") as f:
                f.write(arquivo_audio.getbuffer())
            
            str.info("⏳ Processando arquivo... Enviando para os servidores seguros da IA.")
            
            # Faz o upload seguro para a API do Gemini
            audio_file = genai.upload_file(path=nome_arquivo)
            
            # ESPERA ATÉ O ARQUIVO ESTAR ATIVO (Evita o Erro 400 status ACTIVE)
            str.info("🤖 O Google está processando o formato do arquivo... Aguarde um instante.")
            while audio_file.state.name == "PROCESSING":
                time.sleep(3)
                audio_file = genai.get_file(audio_file.name)
                
            if audio_file.state.name == "FAILED":
                raise Exception("O processamento do arquivo falhou nos servidores da IA.")
            
            str.info("✍️ Aplicando o viés jurídico e formatando o texto...")
            
            # Personaliza a instrução da IA baseado na sua escolha
            if "Ipsis Litteris" in opcao_formato:
                instrucao = (
                    "Você é um transcritor judiciário oficial. Transcreva o áudio a seguir na íntegra, "
                    "mantendo a exata fidelidade das palavras faladas (ideal para termos de depoimento). "
                    "Corrija apenas ruídos extremos, organize em parágrafos lógicos e identifique falantes se houver distinção clara."
                )
            elif "Peça Processual" in opcao_formato:
                instrucao = (
                    "Você é um excelente redator jurídico. Pegue o ditado deste áudio e transforme em um texto técnico, "
                    "formal e polido, adequado para petições ou pareceres. Elimine repetições, gagueiras e termos coloquiais. "
                    "Organize a estrutura em parágrafos jurídicos fluidos e elegantes."
                )
            else:
                instrucao = (
                    "Você é um assistente jurídico de alta performance. Analise o áudio desta audiência/reunião e "
                    "elabore uma ata estruturada contendo: 1) Resumo dos fatos discutidos, 2) Principais teses ou pontos "
                    "levantados e 3) Próximos passos/prazos definidos. Mantenha o tom estritamente profissional."
                )

            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content([instrucao, audio_file])
            
            str.success("🎉 Degravação concluída com sucesso!")
            str.subheader("📄 Documento Jurídico Gerado:")
            str.write(response.text)
            
            str.download_button(
                label="📥 Baixar Documento (.txt)", 
                data=response.text, 
                file_name="degravacao_juridica.txt", 
                mime="text/plain"
            )
            
            # Limpa o arquivo temporário do servidor
            os.remove(nome_arquivo)
            genai.delete_file(audio_file.name)
            
        except Exception as e:
            str.error(f"Ops, ocorreu um erro no processamento: {e}")
            if 'nome_arquivo' in locals() and os.path.exists(nome_arquivo):
                os.remove(nome_arquivo)
    else:
        str.warning("Por favor, selecione ou grave um arquivo de áudio/vídeo primeiro.")
