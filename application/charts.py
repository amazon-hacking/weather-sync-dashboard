import altair as alt

def chart_poluente(df, poluente):
    return alt.Chart(df).mark_bar(color="#4caf50").encode(
        y=alt.Y('bairro:N', sort='-x', title='Bairro'),
        x=alt.X('media_valor:Q', title='Média de Poluentes'),
        tooltip=['bairro', 'media_valor']
    ).properties(
        title=f"Média de {poluente} por bairro",
        width=700,
        height=400
    )

def chart_temperatura(df):
    # Cria uma lista ordenada das datas únicas para manter a ordem cronológica
    if not df.empty and 'data_ordenacao' in df.columns:
        # Ordena pelas datas reais e pega as datas formatadas na ordem correta
        df_sorted = df.sort_values('data_ordenacao')
        date_order = df_sorted['data'].drop_duplicates().tolist()
    else:
        date_order = sorted(df['data'].unique()) if not df.empty else []
    
    return alt.Chart(df).mark_bar().encode(
        x=alt.X("data:N", 
                title="Data", 
                axis=alt.Axis(labelAngle=-45),
                sort=date_order),  # Ordena explicitamente pelas datas
        y=alt.Y("temperatura_media:Q", title="Temperatura Média"),
        color=alt.Color("bairro:N", title="Bairro", scale=alt.Scale(scheme='category10')),
        xOffset="bairro:N",
        tooltip=["data", "bairro", "temperatura_media"]
    ).properties(
        width=max(700, 40 * df['data'].nunique()) if not df.empty else 700,
        height=400,
        title="Temperatura média diária por bairro"
    )

def chart_umidade(df):
    # Mesma lógica para umidade
    if not df.empty and 'data_ordenacao' in df.columns:
        df_sorted = df.sort_values('data_ordenacao')
        date_order = df_sorted['data'].drop_duplicates().tolist()
    else:
        date_order = sorted(df['data'].unique()) if not df.empty else []
    
    return alt.Chart(df).mark_bar().encode(
        x=alt.X("data:N", 
                title="Data", 
                axis=alt.Axis(labelAngle=-45),
                sort=date_order),  # Ordena explicitamente pelas datas
        y=alt.Y("humidade_media:Q", title="Umidade Média"),
        color=alt.Color("bairro:N", title="Bairro", scale=alt.Scale(scheme='category10')),
        xOffset="bairro:N",
        tooltip=["data", "bairro", "humidade_media"],
    ).properties(
        width=max(700, 40 * df['data'].nunique()) if not df.empty else 700,
        height=400,
        title="Umidade média diária por bairro",
    )