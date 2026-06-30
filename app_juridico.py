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

# Interface de Upload
arquivo_audio = str.file_uploader("📂 Selecione o áudio ou vídeo do seu celular:", type=["mp4", "mp3", "wav", "m4a", "aac", "ogg"])

# Opções de formatação jurídica
opcao_formato = str.selectbox(
    "📝 Escolha o tom/formatação do documento:",
    [
        "Transcrição Ipsis Litteris (Padrão de Audiência: Interlocutor - Minutagem - Fala)",
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
            
            # ESPERA ATÉ O ARQUIVO ESTAR ATIVO
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
                    "Você é um transcritor judiciário especialista em audiências trabalhistas e cíveis. "
                    "Sua missão principal é transcrever o áudio na íntegra, com máxima fidelidade e IDENTIFICAR OS PAPÉIS JURÍDICOS dos falantes.\n\n"
                    
                    "RITO E DINÂMICA DA AUDIÊNCIA TRABALHISTA (SIGA ESTA CRONOLOGIA):\n"
                    "1. A PRIMEIRA FALA GERALMENTE É DO JUIZ: Ele inicia o ato, qualifica o depoente e faz as primeiras perguntas que entende pertinentes sobre o caso.\n"
                    "2. REPOSTA DO DEPOENTE: Quem responde logo após as perguntas iniciais do Juiz é o RECLAMANTE ou a TESTEMUNHA.\n"
                    "3. PERGUNTAS DOS ADVOGADOS: Somente após encerrar suas perguntas, o JUIZ passa a palavra para os ADVOGADOS formularem as reperguntas.\n"
                    "4. SISTEMA MEDIADO: O ADVOGADO faz a pergunta ao JUIZ (ex: 'Pergunte se tinha cartão de ponto'), o JUIZ repassa ou refaz a pergunta para o depoente, ou apenas autoriza (ex: 'Pode responder', 'Diga').\n\n"
                    
                    "CRITÉRIOS DE IDENTIFICAÇÃO DOS PAPÉIS:\n"
                    "- JUIZ / JUÍZA: Quem abre a audiência, faz as perguntas iniciais, dita os termos da ata, indefere perguntas e autoriza o depoente a responder.\n"
                    "- ADVOGADO / ADVOGADA: Quem fala apenas após o Juiz franquear a palavra, formulando reperguntas direcionadas à mesa técnica.\n"
                    "- RECLAMANTE / REQUERENTE: O autor da ação que responde diretamente ao Juiz sobre o contrato de trabalho e rotina.\n"
                    "- TESTEMUNHA: A pessoa que presta compromisso legal e responde sobre os fatos que presenciou.\n"
                    "- PREPOSTO / RECLAMADO: Quem responde pela empresa ré.\n\n"
                    
                    "É PROIBIDO usar termos genéricos como 'Interlocutor' ou 'Voz' se pelo contexto da dinâmica acima for possível deduzir o papel do falante.\n\n"
                    
                    "ESTRUTURA DA FORMATAÇÃO (OBRIGATÓRIO LINHA POR LINHA):\n"
                    "Escreva exatamente neste padrão: Papel Identificado - Minutagem [MM:SS] - Texto da fala.\n"
                    "Exemplo:\n"
                    "Juiz - 00:10 - Senhor Reclamante, qual era o seu horário de saída contratual?\n"
                    "Reclamante - 00:14 - Em tese era às 17h, Excelência, mas a gente sempre passava.\n"
                    "Juiz - 00:18 - Palavra deferida ao patrono do reclamante para reperguntas.\n"
                    "Advogado - 00:22 - Excelência, por gentileza, pergunte se o tempo de dobra era registrado no espelho.\n"
                    "Juiz - 00:26 - Havia registro dessas horas extras no ponto? Responda.\n"
                    "Reclamante - 00:29 - Não, o gerente pedia para bater o ponto e voltar para a linha.\n\n"
                    
                    "Não inclua marcações extras como (pergunta) ou (resposta). Apenas o papel, o tempo e a fala exata."
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

            # Mantido a versão 2.5 conforme sua preferência
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
