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
    return alt.Chart(df).mark_bar().encode(
        x=alt.X("data:N", title="Data", axis=alt.Axis(labelAngle=-45)),
        y=alt.Y("temperatura_media:Q", title="Temperatura Média"),
        color=alt.Color("bairro:N", title="Bairro"),
        tooltip=["data", "bairro", "temperatura_media"]
    ).properties(
        width=max(700, 40 * df['data'].nunique()),
        height=400,
        title="Temperatura média diária por bairro"
    )

def chart_umidade(df):
    return alt.Chart(df).mark_bar().encode(
        x=alt.X("data:N", title="Data", axis=alt.Axis(labelAngle=-45)),
        y=alt.Y("humidade_media:Q", title="Umidade Média"),
        color=alt.Color("bairro:N", title="Bairro"),
        xOffset="bairro:N",
        tooltip=["data", "bairro", "humidade_media"]
    ).properties(
        width=max(700, 40 * df['data'].nunique()),
        height=400,
        title="Umidade média diária por bairro"
    )
