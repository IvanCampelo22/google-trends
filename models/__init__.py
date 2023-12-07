from datetime import datetime, timedelta

# Obtém a data atual
data_atual = datetime.now()

# Calcula a data há uma semana atrás
data_uma_semana_atras = data_atual - timedelta(days=7)

# Formata as datas no formato desejado (dia/mês/ano)
data_formatada_atual = data_atual.strftime("%d/%m/%Y")
data_formatada_uma_semana_atras = data_uma_semana_atras.strftime("%d/%m/%Y")

print("Data atual:", data_formatada_atual)
print("Data há uma semana atrás:", data_formatada_uma_semana_atras)