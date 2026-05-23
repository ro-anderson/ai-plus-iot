# Soluções — ex01.ipynb

Cada seção mostra a célula original (com `???` ou trechos faltantes) e logo abaixo a célula resolvida pronta para colar e testar no Jupyter.

---

## Atividade 1 — Leitura e diagnóstico inicial

### Original

```python
# ------------------------------------------------------------
# Atividade 1) Leitura e inspeção inicial
# ------------------------------------------------------------

dados_sujos = pd.read_csv("dados_frota_iot_sujos.csv")

##Implemente os códigos relacionados aos prints abaixo
print("Dimensões da base:")


print("\nPrimeiras linhas:")


print("\nInformações gerais:")


print("\nResumo estatístico das colunas numéricas:")
```

### Solução

```python
# ------------------------------------------------------------
# Atividade 1) Leitura e inspeção inicial
# ------------------------------------------------------------

dados_sujos = pd.read_csv("dados_frota_iot_sujos.csv")

print("Dimensões da base:")
print(dados_sujos.shape)

print("\nPrimeiras linhas:")
display(dados_sujos.head())

print("\nInformações gerais:")
dados_sujos.info()

print("\nResumo estatístico das colunas numéricas:")
display(dados_sujos.describe())
```

---

## Atividade 2 — Diagnóstico de valores ausentes

### Original

```python
# ------------------------------------------------------------
# Atividade 2) Diagnóstico de valores ausentes
# ------------------------------------------------------------
###Implemente o que falta onde aparece ???
ausentes = dados_sujos.???
percentual_ausente = dados_sujos.???

tabela_ausentes = pd.DataFrame({
    "qtd_ausente": ausentes,
    "percentual_ausente": percentual_ausente.round(2)
}).sort_values("percentual_ausente", ascending=False)

display(tabela_ausentes)
```

### Solução

```python
# ------------------------------------------------------------
# Atividade 2) Diagnóstico de valores ausentes
# ------------------------------------------------------------

ausentes = dados_sujos.isna().sum()
percentual_ausente = dados_sujos.isna().mean() * 100

tabela_ausentes = pd.DataFrame({
    "qtd_ausente": ausentes,
    "percentual_ausente": percentual_ausente.round(2)
}).sort_values("percentual_ausente", ascending=False)

display(tabela_ausentes)
```

---

## Atividade 3 — Remoção de duplicatas e atributos pouco úteis

### Original

```python
# ------------------------------------------------------------
# Atividade 3) Remoção de duplicatas e atributos pouco úteis
# ------------------------------------------------------------

###Implemente o que falta onde aparece ???

dados_trabalho = dados_sujos.copy()

print("Dimensões antes da remoção de duplicatas:", dados_trabalho.shape)

dados_trabalho = dados_trabalho.???

print("Dimensões depois da remoção de duplicatas:", dados_trabalho.shape)

n_unicos = dados_trabalho.???
colunas_constantes = list(n_unicos[????].index)

###Identificando colunas com muitos valores ausentes
limite_ausencia = 0.80
percentual_ausente = dados_trabalho.???
colunas_muito_ausentes = list(percentual_ausente[????].index)

colunas_duplicadas_exatas = list(dados_trabalho.columns[????])

colunas_remover = sorted(set(
    colunas_constantes +
    colunas_muito_ausentes +
    colunas_duplicadas_exatas
))

print("\nColunas constantes:", colunas_constantes)
print("Colunas com mais de 80% de ausência:", colunas_muito_ausentes)
print("Colunas duplicadas exatas:", colunas_duplicadas_exatas)
print("\nColunas sugeridas para remoção:", colunas_remover)

##Insira código para remover as colunas em colunas_remover
dados_trabalho = ???

print("\nDimensões após remoção de atributos pouco úteis:", dados_trabalho.shape)

display(dados_trabalho.head())
```

### Solução

```python
# ------------------------------------------------------------
# Atividade 3) Remoção de duplicatas e atributos pouco úteis
# ------------------------------------------------------------

dados_trabalho = dados_sujos.copy()

print("Dimensões antes da remoção de duplicatas:", dados_trabalho.shape)

dados_trabalho = dados_trabalho.drop_duplicates()

print("Dimensões depois da remoção de duplicatas:", dados_trabalho.shape)

n_unicos = dados_trabalho.nunique(dropna=False)
colunas_constantes = list(n_unicos[n_unicos <= 1].index)

limite_ausencia = 0.80
percentual_ausente = dados_trabalho.isna().mean()
colunas_muito_ausentes = list(percentual_ausente[percentual_ausente > limite_ausencia].index)

colunas_duplicadas_exatas = list(dados_trabalho.columns[dados_trabalho.T.duplicated()])

colunas_remover = sorted(set(
    colunas_constantes +
    colunas_muito_ausentes +
    colunas_duplicadas_exatas
))

print("\nColunas constantes:", colunas_constantes)
print("Colunas com mais de 80% de ausência:", colunas_muito_ausentes)
print("Colunas duplicadas exatas:", colunas_duplicadas_exatas)
print("\nColunas sugeridas para remoção:", colunas_remover)

dados_trabalho = dados_trabalho.drop(columns=colunas_remover)

print("\nDimensões após remoção de atributos pouco úteis:", dados_trabalho.shape)

display(dados_trabalho.head())
```

---

## Atividade 5 — Conversão de datas

### Original

```python
# ------------------------------------------------------------
# Atividade 5) Conversão de datas em formatos mistos
# ------------------------------------------------------------

#Apenas entenda e execute o código abaixo

def converter_data_mista(valor):
    if pd.isna(valor):
        return pd.NaT

    formatos = [
        "%d/%m/%Y %H:%M",
        "%Y-%m-%d %H:%M:%S",
        "%m-%d-%Y %H:%M"
    ]

    for formato in formatos:
        data = pd.to_datetime(???)
        if not pd.isna(data):
            return data

    return pd.NaT


dados_datas = dados_categorias.copy()
dados_datas["data_viagem_convertida"] = dados_datas["data_viagem"].apply(converter_data_mista)

print("Quantidade de datas inválidas após conversão:")
print(dados_datas["data_viagem_convertida"].isna().sum())

display(dados_datas[["data_viagem", "data_viagem_convertida"]].head(12))

dados_datas = dados_datas.drop(columns=["data_viagem"])
dados_datas = dados_datas.rename(columns={"data_viagem_convertida": "data_viagem"})

print("\nTipo da coluna data_viagem após conversão:")
print(dados_datas["data_viagem"].dtype)
```

### Solução

```python
# ------------------------------------------------------------
# Atividade 5) Conversão de datas em formatos mistos
# ------------------------------------------------------------

# Apenas entenda e execute o código abaixo
# OBS: identificamos uma inconsistência neste enunciado — apesar de pedir
# apenas execução, a célula contém um ??? em pd.to_datetime(???) que
# precisa ser preenchido. Solução aplicada abaixo.

def converter_data_mista(valor):
    if pd.isna(valor):
        return pd.NaT

    formatos = [
        "%d/%m/%Y %H:%M",
        "%Y-%m-%d %H:%M:%S",
        "%m-%d-%Y %H:%M"
    ]

    for formato in formatos:
        # Trecho corrigido: passamos o valor, o formato atual da iteração
        # e errors="coerce" para que datas inválidas virem NaT em vez de
        # lançar exceção, permitindo testar o próximo formato da lista.
        data = pd.to_datetime(valor, format=formato, errors="coerce")
        if not pd.isna(data):
            return data

    return pd.NaT


dados_datas = dados_categorias.copy()
dados_datas["data_viagem_convertida"] = dados_datas["data_viagem"].apply(converter_data_mista)

print("Quantidade de datas inválidas após conversão:")
print(dados_datas["data_viagem_convertida"].isna().sum())

display(dados_datas[["data_viagem", "data_viagem_convertida"]].head(12))

dados_datas = dados_datas.drop(columns=["data_viagem"])
dados_datas = dados_datas.rename(columns={"data_viagem_convertida": "data_viagem"})

print("\nTipo da coluna data_viagem após conversão:")
print(dados_datas["data_viagem"].dtype)
```

---

## Atividade 7 — Tratamento de inconsistências físicas

### Original

```python
# ------------------------------------------------------------
# Atividade 7) Tratamento de inconsistências físicas
# ------------------------------------------------------------

###Implemente o que falta onde aparece ???

dados_consistentes = dados_unidades.copy()

regras = {
    "distancia_km": ??? "distancia_km" > 0??
    "combustivel_litros": ???"combustivel_litros" > 0???,
    "velocidade_media_kmh": ??? "velocidade_media_kmh entre 0 e  130" ???,
    "temperatura_motor_c": "temperatura_motor_c entre 40 e  130"???,
    "vibracao_motor_mm_s": "vibracao_motor_mm_s" > 0,
    "frenagens_bruscas": "frenagens_bruscas" >= 0,
    "tempo_viagem_min": "tempo_viagem_min" > 0
}

for coluna, mascara_valida in regras.items():
    qtd_invalidos_ou_ausentes = (~mascara_valida.fillna(False)).sum()
    print(f"{coluna}: {qtd_invalidos_ou_ausentes} valores inválidos ou ausentes pela regra")
    dados_consistentes.loc[~mascara_valida.fillna(False), coluna] = np.nan

print("\nValores ausentes após aplicar regras de consistência em ordem decrescente:")
display(dados_consistentes.isna().sum().????))
```

### Solução

```python
# ------------------------------------------------------------
# Atividade 7) Tratamento de inconsistências físicas
# ------------------------------------------------------------

dados_consistentes = dados_unidades.copy()

regras = {
    "distancia_km": dados_consistentes["distancia_km"] > 0,
    "combustivel_litros": dados_consistentes["combustivel_litros"] > 0,
    "velocidade_media_kmh": dados_consistentes["velocidade_media_kmh"].between(0, 130),
    "temperatura_motor_c": dados_consistentes["temperatura_motor_c"].between(40, 130),
    "vibracao_motor_mm_s": dados_consistentes["vibracao_motor_mm_s"] > 0,
    "frenagens_bruscas": dados_consistentes["frenagens_bruscas"] >= 0,
    "tempo_viagem_min": dados_consistentes["tempo_viagem_min"] > 0
}

for coluna, mascara_valida in regras.items():
    qtd_invalidos_ou_ausentes = (~mascara_valida.fillna(False)).sum()
    print(f"{coluna}: {qtd_invalidos_ou_ausentes} valores inválidos ou ausentes pela regra")
    dados_consistentes.loc[~mascara_valida.fillna(False), coluna] = np.nan

print("\nValores ausentes após aplicar regras de consistência em ordem decrescente:")
display(dados_consistentes.isna().sum().sort_values(ascending=False))
```

---

## Atividade 8 — Imputação de valores ausentes

### Original

```python
# ------------------------------------------------------------
# Atividade 8) Imputação de valores ausentes
# ------------------------------------------------------------

###Implemente o que falta onde aparece ???

dados_imputados = dados_consistentes.copy()

colunas_mediana = [
    "distancia_km",
    "combustivel_litros",
    "velocidade_media_kmh",
    "temperatura_motor_c",
    "vibracao_motor_mm_s",
    "frenagens_bruscas",
    "tempo_viagem_min",
    "consumo_km_l"
]

for coluna in colunas_mediana:
    mediana = ???
    dados_imputados[coluna] = ??? #Imputar mediana
    print(f"{coluna}: ausentes imputados com mediana = {mediana:.2f}")

for coluna in ["status_manutencao", "tipo_veiculo", "risco_falha"]:
    moda = ???
    dados_imputados[coluna] = ??? #Imputar moda
    print(f"{coluna}: ausentes imputados com moda = {moda}")

print("\nValores ausentes após imputação:")
display(dados_imputados.isna().sum().sort_values(ascending=False))

# Atividade para o aluno:
# Escolha uma variável e compare describe() antes e depois da imputação.
```

### Solução

```python
# ------------------------------------------------------------
# Atividade 8) Imputação de valores ausentes
# ------------------------------------------------------------

dados_imputados = dados_consistentes.copy()

colunas_mediana = [
    "distancia_km",
    "combustivel_litros",
    "velocidade_media_kmh",
    "temperatura_motor_c",
    "vibracao_motor_mm_s",
    "frenagens_bruscas",
    "tempo_viagem_min",
    "consumo_km_l"
]

for coluna in colunas_mediana:
    mediana = dados_imputados[coluna].median()
    dados_imputados[coluna] = dados_imputados[coluna].fillna(mediana)
    print(f"{coluna}: ausentes imputados com mediana = {mediana:.2f}")

for coluna in ["status_manutencao", "tipo_veiculo", "risco_falha"]:
    moda = dados_imputados[coluna].mode().iloc[0]
    dados_imputados[coluna] = dados_imputados[coluna].fillna(moda)
    print(f"{coluna}: ausentes imputados com moda = {moda}")

print("\nValores ausentes após imputação:")
display(dados_imputados.isna().sum().sort_values(ascending=False))

# Comparação describe() antes e depois — exemplo com distancia_km
print("\nAntes da imputação (distancia_km):")
display(dados_consistentes["distancia_km"].describe())

print("\nDepois da imputação (distancia_km):")
display(dados_imputados["distancia_km"].describe())
```

---

## Atividade 9 — Remoção de atributos redundantes ou irrelevantes

### Original

```python
# ------------------------------------------------------------
# Atividade 9) Análise de redundância e remoção de atributos
# ------------------------------------------------------------

###Implemente o que falta onde aparece ???

dados_sem_irrelevantes = dados_imputados.copy()

colunas_numericas = dados_sem_irrelevantes.select_dtypes(include="number").columns

plt.figure(figsize=(10, 7))
sns.heatmap(
    dados_sem_irrelevantes[colunas_numericas].corr(),
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    vmin=-1,
    vmax=1
)
plt.title("Correlação entre variáveis numéricas")
plt.show()

colunas_remover_modelagem = [
    "id_viagem",
    "codigo_sensor_aleatorio",
    "distancia_km_backup"
]

dados_sem_irrelevantes = dados_sem_irrelevantes.drop(????)

print("Colunas removidas:", colunas_remover_modelagem)
print("Dimensões após remoção:", dados_sem_irrelevantes.shape)

display(dados_sem_irrelevantes.head())
```

### Solução

```python
# ------------------------------------------------------------
# Atividade 9) Análise de redundância e remoção de atributos
# ------------------------------------------------------------

dados_sem_irrelevantes = dados_imputados.copy()

colunas_numericas = dados_sem_irrelevantes.select_dtypes(include="number").columns

plt.figure(figsize=(10, 7))
sns.heatmap(
    dados_sem_irrelevantes[colunas_numericas].corr(),
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    vmin=-1,
    vmax=1
)
plt.title("Correlação entre variáveis numéricas")
plt.show()

colunas_remover_modelagem = [
    "id_viagem",
    "codigo_sensor_aleatorio",
    "distancia_km_backup"
]

dados_sem_irrelevantes = dados_sem_irrelevantes.drop(columns=colunas_remover_modelagem)

print("Colunas removidas:", colunas_remover_modelagem)
print("Dimensões após remoção:", dados_sem_irrelevantes.shape)

display(dados_sem_irrelevantes.head())
```

---

## Atividade 10 — Outliers com IQR

### Original

```python
# ------------------------------------------------------------
# Atividade 10) Detecção de outliers com IQR
# ------------------------------------------------------------

###Implemente o que falta onde aparece ???

def criar_mascara_sem_outliers_iqr(df, colunas, fator=1.5):
    mascara_final = pd.Series(True, index=df.index)

    for coluna in colunas:
        q1 = df[coluna].???
        q3 = df[coluna].???
        iqr =???

        limite_inferior = ?? - fator * ??
        limite_superior = ?? + fator * ??

        mascara_coluna = df[coluna].between(??, ??)

        qtd_outliers = (~mascara_coluna).sum()
        print(f"{coluna}: {qtd_outliers} outliers pelo IQR com fator={fator}")

        mascara_final = mascara_final & mascara_coluna

    return mascara_final


colunas_outliers = [
    "vibracao_motor_mm_s",
    "frenagens_bruscas",
    "temperatura_motor_c",
    "combustivel_litros"
]

dados_base_outliers = dados_sem_irrelevantes.copy()

mascara_iqr = criar_mascara_sem_outliers_iqr(
    dados_base_outliers,
    colunas=colunas_outliers,
    fator=1.5
)

dados_iqr = dados_base_outliers[mascara_iqr].copy()

print("\nLinhas antes:", dados_base_outliers.shape[0])
print("Linhas depois do IQR:", dados_iqr.shape[0])
print("Linhas removidas:", dados_base_outliers.shape[0] - dados_iqr.shape[0])
```

### Solução

```python
# ------------------------------------------------------------
# Atividade 10) Detecção de outliers com IQR
# ------------------------------------------------------------

def criar_mascara_sem_outliers_iqr(df, colunas, fator=1.5):
    mascara_final = pd.Series(True, index=df.index)

    for coluna in colunas:
        q1 = df[coluna].quantile(0.25)
        q3 = df[coluna].quantile(0.75)
        iqr = q3 - q1

        limite_inferior = q1 - fator * iqr
        limite_superior = q3 + fator * iqr

        mascara_coluna = df[coluna].between(limite_inferior, limite_superior)

        qtd_outliers = (~mascara_coluna).sum()
        print(f"{coluna}: {qtd_outliers} outliers pelo IQR com fator={fator}")

        mascara_final = mascara_final & mascara_coluna

    return mascara_final


colunas_outliers = [
    "vibracao_motor_mm_s",
    "frenagens_bruscas",
    "temperatura_motor_c",
    "combustivel_litros"
]

dados_base_outliers = dados_sem_irrelevantes.copy()

mascara_iqr = criar_mascara_sem_outliers_iqr(
    dados_base_outliers,
    colunas=colunas_outliers,
    fator=1.5
)

dados_iqr = dados_base_outliers[mascara_iqr].copy()

print("\nLinhas antes:", dados_base_outliers.shape[0])
print("Linhas depois do IQR:", dados_iqr.shape[0])
print("Linhas removidas:", dados_base_outliers.shape[0] - dados_iqr.shape[0])
```

---

## Atividade 11 — Outliers com z-score

### Original

```python
# ------------------------------------------------------------
# Atividade 11) Detecção de outliers com z-score
# ------------------------------------------------------------

###Implemente o que falta onde aparece ???

dados_zscore_base = dados_base_outliers.copy()

limite_z = 3.0

z = dados_zscore_base[colunas_outliers].apply(???)

mascara_sem_outlier_z = (np.abs(z) <=???).all(axis=1)

dados_zscore_filtrado = dados_zscore_base[???].copy()

print("Linhas antes:", dados_zscore_base.shape[0])
print("Linhas depois do z-score:", dados_zscore_filtrado.shape[0])
print("Linhas removidas:", dados_zscore_base.shape[0] - dados_zscore_filtrado.shape[0])

# Atividade para o aluno:
# Altere limite_z para 2.5 e compare os resultados.
```

### Solução

```python
# ------------------------------------------------------------
# Atividade 11) Detecção de outliers com z-score
# ------------------------------------------------------------

dados_zscore_base = dados_base_outliers.copy()

limite_z = 3.0

z = dados_zscore_base[colunas_outliers].apply(zscore, nan_policy="omit")

mascara_sem_outlier_z = (np.abs(z) <= limite_z).all(axis=1)

dados_zscore_filtrado = dados_zscore_base[mascara_sem_outlier_z].copy()

print("Linhas antes:", dados_zscore_base.shape[0])
print("Linhas depois do z-score:", dados_zscore_filtrado.shape[0])
print("Linhas removidas:", dados_zscore_base.shape[0] - dados_zscore_filtrado.shape[0])

# Comparação com limite_z = 2.5
limite_z_2 = 2.5
mascara_z_2 = (np.abs(z) <= limite_z_2).all(axis=1)
dados_zscore_filtrado_2 = dados_zscore_base[mascara_z_2].copy()
print("\nCom limite_z = 2.5:")
print("Linhas depois:", dados_zscore_filtrado_2.shape[0])
print("Linhas removidas:", dados_zscore_base.shape[0] - dados_zscore_filtrado_2.shape[0])
```

---

## Atividade 12 — Outliers com DBSCAN

### Original

```python
# ------------------------------------------------------------
# Atividade 12) Detecção de outliers com DBSCAN
# ------------------------------------------------------------

###Implemente o que falta onde aparece ???

dados_dbscan_base = dados_base_outliers.copy()

colunas_dbscan = [
    "distancia_km",
    "combustivel_litros",
    "velocidade_media_kmh",
    "temperatura_motor_c",
    "vibracao_motor_mm_s",
    "frenagens_bruscas",
    "tempo_viagem_min"
]

scaler = StandardScaler()
X_dbscan = scaler.fit_transform(dados_dbscan_base[???])

dbscan = DBSCAN(eps=1.8, min_samples=8)
rotulos = dbscan.fit_predict(???)

dados_dbscan_base["cluster_dbscan"] = rotulos
dados_dbscan_base["outlier_dbscan"] = dados_dbscan_base["cluster_dbscan"] == -1

print("Contagem de rótulos do DBSCAN:")
display(dados_dbscan_base[???].value_counts().sort_index())

print("\nQuantidade de outliers pelo DBSCAN:")
print(dados_dbscan_base[???].sum())

dados_dbscan_filtrado = dados_dbscan_base[~dados_dbscan_base["outlier_dbscan"]].copy()
dados_dbscan_filtrado = dados_dbscan_filtrado.drop(columns=["cluster_dbscan", "outlier_dbscan"])

print("\nLinhas antes:", dados_dbscan_base.shape[0])
print("Linhas depois do DBSCAN:", dados_dbscan_filtrado.shape[0])
```

### Solução

```python
# ------------------------------------------------------------
# Atividade 12) Detecção de outliers com DBSCAN
# ------------------------------------------------------------

dados_dbscan_base = dados_base_outliers.copy()

colunas_dbscan = [
    "distancia_km",
    "combustivel_litros",
    "velocidade_media_kmh",
    "temperatura_motor_c",
    "vibracao_motor_mm_s",
    "frenagens_bruscas",
    "tempo_viagem_min"
]

scaler = StandardScaler()
X_dbscan = scaler.fit_transform(dados_dbscan_base[colunas_dbscan])

dbscan = DBSCAN(eps=1.8, min_samples=8)
rotulos = dbscan.fit_predict(X_dbscan)

dados_dbscan_base["cluster_dbscan"] = rotulos
dados_dbscan_base["outlier_dbscan"] = dados_dbscan_base["cluster_dbscan"] == -1

print("Contagem de rótulos do DBSCAN:")
display(dados_dbscan_base["cluster_dbscan"].value_counts().sort_index())

print("\nQuantidade de outliers pelo DBSCAN:")
print(dados_dbscan_base["outlier_dbscan"].sum())

dados_dbscan_filtrado = dados_dbscan_base[~dados_dbscan_base["outlier_dbscan"]].copy()
dados_dbscan_filtrado = dados_dbscan_filtrado.drop(columns=["cluster_dbscan", "outlier_dbscan"])

print("\nLinhas antes:", dados_dbscan_base.shape[0])
print("Linhas depois do DBSCAN:", dados_dbscan_filtrado.shape[0])
```

---

## Atividade 14 — Salvamento da base limpa

> Observação: a célula original tem a linha `Apenas execute o código a seguir` sem o `#`, o que causa **SyntaxError**. A solução abaixo já corrige.

### Original

```python
# ------------------------------------------------------------
# Atividade 14) Salvamento da base limpa
# ------------------------------------------------------------

Apenas execute o código a seguir

dados_finais = dados_iqr.copy()

nome_saida = "dados_frota_iot_limpos.csv"
dados_finais.to_csv(nome_saida, index=False)

print(f"Base limpa salva em: {nome_saida}")
print("Dimensões da base final:", dados_finais.shape)

display(dados_finais.head())
```

### Solução

```python
# ------------------------------------------------------------
# Atividade 14) Salvamento da base limpa
# ------------------------------------------------------------

# Apenas execute o código a seguir

dados_finais = dados_iqr.copy()

nome_saida = "dados_frota_iot_limpos.csv"
dados_finais.to_csv(nome_saida, index=False)

print(f"Base limpa salva em: {nome_saida}")
print("Dimensões da base final:", dados_finais.shape)

display(dados_finais.head())
```

---

## Atividade 15 — Preparação para as próximas aulas

### Original

```python
# ------------------------------------------------------------
# Atividade 15) Preparação para transformação e modelagem
# ------------------------------------------------------------

print("Colunas da base final:")
print(list(dados_finais.columns))

print("\nTipos das colunas:")
display(dados_finais.dtypes)

print("\nColunas categóricas:")
colunas_categoricas = list(dados_finais.select_dtypes(include="object").columns)
print(colunas_categoricas)

print("\nColunas numéricas:")
colunas_numericas = list(dados_finais.select_dtypes(include="number").columns)
print(colunas_numericas)

# Atividade para o aluno:
# Preencha estas listas com base na interpretação do problema.

categoricas_para_encoding = [
    # exemplo: "tipo_veiculo",
    # complete aqui
]

numericas_para_escalonamento = [
    # exemplo: "distancia_km",
    # complete aqui
]

possivel_alvo_classificacao = "risco_falha"
possivel_alvo_regressao = "combustivel_litros"

print("\nPossível alvo de classificação:", possivel_alvo_classificacao)
print("Possível alvo de regressão:", possivel_alvo_regressao)
```

### Solução

```python
# ------------------------------------------------------------
# Atividade 15) Preparação para transformação e modelagem
# ------------------------------------------------------------

print("Colunas da base final:")
print(list(dados_finais.columns))

print("\nTipos das colunas:")
display(dados_finais.dtypes)

print("\nColunas categóricas:")
colunas_categoricas = list(dados_finais.select_dtypes(include="object").columns)
print(colunas_categoricas)

print("\nColunas numéricas:")
colunas_numericas = list(dados_finais.select_dtypes(include="number").columns)
print(colunas_numericas)

categoricas_para_encoding = [
    "veiculo",
    "tipo_veiculo",
    "motorista",
    "status_manutencao",
]

numericas_para_escalonamento = [
    "distancia_km",
    "combustivel_litros",
    "velocidade_media_kmh",
    "temperatura_motor_c",
    "vibracao_motor_mm_s",
    "frenagens_bruscas",
    "tempo_viagem_min",
    "consumo_km_l",
]

possivel_alvo_classificacao = "risco_falha"
possivel_alvo_regressao = "combustivel_litros"

print("\nPossível alvo de classificação:", possivel_alvo_classificacao)
print("Possível alvo de regressão:", possivel_alvo_regressao)
```
