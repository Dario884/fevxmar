import pandas as pd
import plotly.express as px
import random 
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import Dash,html,dcc,Input,Output
import datetime
import math
import os

d1 = pd.read_excel('Vendas.xlsx')
d2 = pd.read_excel('Vendas - Dez.xlsx')

# dia da semana
def dia(a,m,d):
    """recebe o ano, mês e dia de uma data
    e retorna o nome do dia da semana"""
    dia = datetime.date.today().day
    sem = ("Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo")
    num = datetime.date(a, m, d).weekday()
    return sem[num]
# d1
d1['Data']=pd.to_datetime(d1['Data'])
d1['Ano']=d1['Data'].dt.year
d1['Mês']=d1['Data'].dt.month
d1['Dia']=d1['Data'].dt.day
for ind in list(d1.index):
    d1.loc[ind,'Dia da semana']=dia(d1.loc[ind,'Ano'], d1.loc[ind,'Mês'], d1.loc[ind,'Dia'])
# d2
d2['Data']=pd.to_datetime(d2['Data'])
d2['Ano']=d2['Data'].dt.year
d2['Mês']=d2['Data'].dt.month
d2['Dia']=d2['Data'].dt.day
for ind in list(d2.index):
    d2.loc[ind,'Dia da semana']=dia(d2.loc[ind,'Ano'], d2.loc[ind,'Mês'], d2.loc[ind,'Dia'])

# sexo do comprador
for c in range(0,93910):
    if c<63910:
        d1.loc[c,'Sexo']='Mulher'
    else:
        d1.loc[c,'Sexo']='Homem'
for c in range(0,7089):
    if c<4089:
        d2.loc[c,'Sexo']='Mulher'
    else:
        d2.loc[c,'Sexo']='Homem'
# idade do comprador
idades=[]
for c in range(0,20000):
    idades.append(random.randint(18,25))
for c in range(0,40000):
    idades.append(random.randint(26,35))
for c in range(0,20000):
    idades.append(random.randint(36,45))
for c in range(0,13910):
    idades.append(random.randint(46,65))
for c in range(0,93910):
    d1.loc[c,'Idade']= random.choice(idades)
for c in range(0,7089):
    d2.loc[c,'Idade']= random.choice(idades)

# metodos de pagamento
pag = ['Pix','Crédito','Débito','Dinheiro']
for c in range(0,93910):
    d1.loc[c,'Pagamento']=random.choice(pag)
for c in range(0,7089):
    d2.loc[c,'Pagamento']=random.choice(pag)
# custo
for c in range(0,93910):
    n = random.randint(10,60)
    d1.loc[c,'Custo']=d1.loc[c,'Valor Unitário']*(n/100)
for c in range(0,7089):
    n = random.randint(10,60)
    d2.loc[c,'Custo']=d2.loc[c,'Valor Unitário']*(n/100)
dados = pd.concat([d1,d2], axis=0)
# data
dados['Data']=pd.to_datetime(dados['Data'])
dados['Mês']=dados['Data'].dt.month
# lucro
dados['Lucro']=dados['Valor Final']-(dados['Custo']*dados['Quantidade'])

lojas = ['Shopping Vila Velha','Norte Shopping','Iguatemi Campinas','Salvador Shopping','Bourbon Shopping SP']
dados.rename(columns={'ID Loja':'Loja'}, inplace=True)
vendasinit = dados.query('Loja in ["Shopping Vila Velha","Norte Shopping","Iguatemi Campinas","Salvador Shopping","Bourbon Shopping SP"]')
vendasf = vendasinit.query('Mês == 2')
vendasm = vendasinit.query('Mês == 3')

fatfev = vendasf[['Dia','Valor Final','Lucro']].groupby('Dia').sum()
fatmar = vendasm[['Dia','Valor Final','Lucro']].groupby('Dia').sum()

for d in list(fatfev.index):
    fatfev.loc[d,'Dia']=d
fatfev['Mês']='Fevereiro'
for d in list(fatmar.index):
    fatmar.loc[d,'Dia']=d
fatmar['Mês']='Março'

qfev = vendasf['Dia'].value_counts()
qmar = vendasm['Dia'].value_counts()
for i in list(fatfev.index):
    fatfev.loc[i,'Quantidade de vendas']=qfev[i]
fatfev['Ticket']=fatfev['Valor Final']/fatfev['Quantidade de vendas']
ticfev=fatfev['Ticket'].mean()

for i in list(fatmar.index):
    fatmar.loc[i,'Quantidade de vendas']=qmar[i]
fatmar['Ticket']=fatmar['Valor Final']/fatmar['Quantidade de vendas']
ticmar=fatmar['Ticket'].mean()
compfat = pd.concat([fatfev,fatmar], axis=0)
compfat.rename(columns={'Valor Final':'Faturamento diário','Lucro':'Lucro diário'}, inplace=True)
# comp do fat/luc por dia (dife)
totalfatfev = fatfev['Valor Final'].sum()
totalfatmar = fatmar['Valor Final'].sum()
totallucfev = fatfev['Lucro'].sum()
totallucmar = fatmar['Lucro'].sum()
difefat = totalfatmar-totalfatfev
difeluc = totallucmar-totallucfev
if totalfatmar<totalfatfev:
    graffat = px.line(compfat, x='Dia', y='Faturamento diário', color='Mês', template='plotly_dark', color_discrete_sequence=['cyan','white'],
                  title=f'Comparação do faturamento diário (R${(-1)*difefat} a menos que em Fevereiro)')
if totalfatmar>totalfatfev:
    graffat = px.line(compfat, x='Dia', y='Faturamento diário', color='Mês', template='plotly_dark', color_discrete_sequence=['cyan','white'],
                  title=f'Comparação do faturamento diário (R${difefat} a mais que em Fevereiro)')
if totallucmar<totallucfev:
    grafluc = px.line(compfat, x='Dia', y='Lucro diário', color='Mês', template='plotly_dark', color_discrete_sequence=['darkcyan','white'],
                  title=f'Comparação do lucro diário (R${(-1)*difeluc} a menos que em Fevereiro)')
if totallucmar>totallucfev:
    grafluc = px.line(compfat, x='Dia', y='Lucro diário', color='Mês', template='plotly_dark', color_discrete_sequence=['red','white'],
                  title=f'Comparação do lucro diário (R${difeluc:.0f} a mais que em Fevereiro)')

# comp do ticket médio (dife)
difetic = ticmar-ticfev
quantf = vendasf[['Produto','Quantidade']].groupby('Produto').sum()
quantm = vendasm[['Produto','Quantidade']].groupby('Produto').sum()
totpfev = quantf['Quantidade'].sum()
totpmar = quantm['Quantidade'].sum()
sub3 = make_subplots(rows=2, cols=3, specs=[[{'rowspan':2,'type':'domain'}, {'rowspan':2,'type':'domain'}, {'rowspan':2,'type':'xy'}],
                                           [None,None,None]], subplot_titles=[f'{totpfev} vendidos em fevereiro',f'{totpmar} vendidos em março',f'Ticket médio (R${difetic:.2f}+)'])
sub3.update_layout(template='plotly_dark')
sub3.update_annotations(font_size=20)
sub3.add_trace(go.Bar(x=['Fevereiro','Março'], y=[ticfev, ticmar], marker=dict(color=['cyan','white']),
                     legendgroup='Meses'), row=1, col=3)

berq = 0
calq = 0
camq = 0
camsq = 0
casaq = 0
chinq = 0
cintq = 0
cuecq = 0
gorq = 0
meiq = 0
mochq = 0
polq = 0
pulq = 0
relq = 0
sapq = 0
shoq = 0
sungq = 0
terq = 0
teniq = 0

ber = 0
cal = 0
cam = 0
cams = 0
casa = 0
chin = 0
cint= 0
cuec = 0
gor = 0
mei = 0
moch = 0
pol = 0
pul = 0
rel = 0
sap = 0
sho = 0
sung = 0
ter = 0
teni = 0
for n in list(quantf.index):
    if 'Bermuda' in n:
        berq = berq + quantf.loc[n,'Quantidade']
    if 'Calça' in n:
        calq = calq + quantf.loc[n,'Quantidade']
    if 'Camisa' in n:
        camq = camq + quantf.loc[n,'Quantidade']
    if 'Camiseta' in n:
        camsq = camsq + quantf.loc[n,'Quantidade']
    if 'Casaco' in n:
        casaq = casaq + quantf.loc[n,'Quantidade']
    if 'Chinelo' in n:
        chinq = chinq + quantf.loc[n,'Quantidade']
    if 'Cinto' in n:
        cintq = cintq + quantf.loc[n,'Quantidade']
    if 'Cueca' in n:
        cuecq = cuecq + quantf.loc[n,'Quantidade']
    if 'Gorro' in n:
        gorq = gorq + quantf.loc[n,'Quantidade']
    if 'Meia' in n:
        meiq = meiq + quantf.loc[n,'Quantidade']
    if 'Mochila' in n:
        mochq = mochq + quantf.loc[n,'Quantidade']
    if 'Polo' in n:
        polq = polq + quantf.loc[n,'Quantidade']
    if 'Pulseira' in n:
        pulq = pulq + quantf.loc[n,'Quantidade']
    if 'Relógio' in n:
        relq = relq + quantf.loc[n,'Quantidade']
    if 'Sapato' in n:
        sapq = sapq + quantf.loc[n,'Quantidade']
    if 'Short' in n:
        shoq = shoq + quantf.loc[n,'Quantidade']
    if 'Sunga' in n:
        sungq = sungq + quantf.loc[n,'Quantidade']
    if 'Terno' in n:
        terq = terq + quantf.loc[n,'Quantidade']
    if 'Tênis' in n:
        teniq = teniq + quantf.loc[n,'Quantidade']
for n in list(quantm.index):
    if 'Bermuda' in n:
        ber = ber + quantm.loc[n,'Quantidade']
    if 'Calça' in n:
        cal = cal + quantm.loc[n,'Quantidade']
    if 'Camisa' in n:
        cam = cam + quantm.loc[n,'Quantidade']
    if 'Camiseta' in n:
        cams = cams + quantm.loc[n,'Quantidade']
    if 'Casaco' in n:
        casa = casa + quantm.loc[n,'Quantidade']
    if 'Chinelo' in n:
        chin = chin + quantm.loc[n,'Quantidade']
    if 'Cinto' in n:
        cint = cint + quantm.loc[n,'Quantidade']
    if 'Cueca' in n:
        cuec = cuec + quantm.loc[n,'Quantidade']
    if 'Gorro' in n:
        gor = gor + quantm.loc[n,'Quantidade']
    if 'Meia' in n:
        mei = mei + quantm.loc[n,'Quantidade']
    if 'Mochila' in n:
        moch = moch + quantm.loc[n,'Quantidade']
    if 'Polo' in n:
        pol = pol + quantm.loc[n,'Quantidade']
    if 'Pulseira' in n:
        pul = pul + quantm.loc[n,'Quantidade']
    if 'Relógio' in n:
        rel = rel + quantm.loc[n,'Quantidade']
    if 'Sapato' in n:
        sap = sap + quantm.loc[n,'Quantidade']
    if 'Short' in n:
        sho = sho + quantm.loc[n,'Quantidade']
    if 'Sunga' in n:
        sung = sung + quantm.loc[n,'Quantidade']
    if 'Terno' in n:
        ter = ter + quantm.loc[n,'Quantidade']
    if 'Tênis' in n:
        teni = teni + quantm.loc[n,'Quantidade']

dic = {}
dic['Bermuda']=berq
dic['Calça']=calq
dic['Camisa']=camq
dic['Camiseta']=camsq
dic['Casaco']=casaq
dic['Chinelo']=chinq
dic['Cinto']=cintq
dic['Cueca']=cuecq
dic['Gorro']=gorq
dic['Meia']=meiq
dic['Mochila']=mochq
dic['Polo']=polq
dic['Pulseira']=pulq
dic['Relógio']=relq
dic['Sapato']=sapq
dic['Short']=shoq
dic['Sunga']=sungq
dic['Terno']=terq
dic['Tênis']=teniq

dic1 = {}
dic1['Bermuda']=ber
dic1['Calça']=cal
dic1['Camisa']=cam
dic1['Camiseta']=cams
dic1['Casaco']=casa
dic1['Chinelo']=chin
dic1['Cinto']=cint
dic1['Cueca']=cuec
dic1['Gorro']=gor
dic1['Meia']=mei
dic1['Mochila']=moch
dic1['Polo']=pol
dic1['Pulseira']=pul
dic1['Relógio']=rel
dic1['Sapato']=sap
dic1['Short']=sho
dic1['Sunga']=sung
dic1['Terno']=ter
dic1['Tênis']=teni
sub3.add_trace(go.Pie(labels=list(dic.keys()), values=list(dic.values()), hole=0.3), row=1, col=1)
sub3.add_trace(go.Pie(labels=list(dic1.keys()), values=list(dic1.values()), hole=0.3), row=1, col=2)

# vendas ao longo dos dois meses
quantvd = make_subplots(rows=2, cols=2, specs=[[{'rowspan':2,'type':'xy'}, {'rowspan':2,'type':'xy'}],
                                              [None, None]], subplot_titles=['Volume de vendas em fev.','Volume de vendas em mar.'],
                       shared_yaxes=True)
quantvd.update_layout(template='plotly_dark')
quantvd.update_annotations(font_size=20)
quantvd.add_trace(go.Bar(x=list(fatfev['Dia']), y=list(fatfev['Quantidade de vendas']), name='Dias de fevereiro', marker=dict(color='cyan')), row=1, col=1)
quantvd.add_trace(go.Bar(x=list(fatmar['Dia']), y=list(fatmar['Quantidade de vendas']), name='Dias de Março', marker=dict(color='red')), row=1, col=2)
quantvd.update_yaxes(title_text='Quantidade de vendas', row=1, col=1)
quantvd.update_yaxes(title_text='Quantidade de vendas', row=1, col=2)
quantvd.update_xaxes(title_text='Dia', row=1, col=1)
quantvd.update_xaxes(title_text='Dia', row=1, col=2)

# prod mais/menos vendidos nesse bimestre
vendasfm = pd.concat([vendasf, vendasm], axis=0)
topprod = vendasfm[['Produto','Quantidade']].groupby('Produto').sum()
x=[]
y=[]
x1=[]
y1=[]
for c in range(0,10):
    x.append(topprod.idxmax().to_dict()['Quantidade'])
    y.append(topprod.max().to_dict()['Quantidade'])
    for i in list(topprod.index):
        if topprod.loc[i,'Quantidade']==topprod.max().to_dict()['Quantidade']:
            topprod = topprod.drop(i)
            break
dicp = {}
dicp['Produtos']=x
dicp['Quantidade']=y
datap = pd.DataFrame(dicp)
datap.rename(columns={'Quantidade':'Quantidade vendida'}, inplace=True)
top = px.bar(datap, x='Produtos', y='Quantidade vendida', template='plotly_dark', color_discrete_sequence=['cyan','cyan','cyan','cyan','cyan','cyan','cyan','cyan','cyan','cyan'],
            title='Produtos mais vendidos nesse bimestre', height=600)

for c in range(0,10):
    x1.append(topprod.idxmin().to_dict()['Quantidade'])
    y1.append(topprod.min().to_dict()['Quantidade'])
    for i in list(topprod.index):
        if topprod.loc[i,'Quantidade']==topprod.min().to_dict()['Quantidade']:
            topprod = topprod.drop(i)
            break
dicp1 = {}
dicp1['Produtos']=x1
dicp1['Quantidade']=y1
datap1 = pd.DataFrame(dicp1)
datap1.rename(columns={'Quantidade':'Quantidade vendida'}, inplace=True)
low = px.bar(datap1, x='Produtos', y='Quantidade vendida', template='plotly_dark', color_discrete_sequence=['red','red','red','red','red','red','red','red','red','red'],
            title='Produtos menos vendidos nesse bimestre', height=400)

sub6 = make_subplots(rows=2, cols=2, specs=[[{'rowspan':2,'type':'xy'}, {'rowspan':2,'type':'domain'}],
                                           [None, None]], subplot_titles=['5 produtos com maior faturamento (bimestre)','Vendas X Canal (bimestre)'])
sub6.update_layout(template='plotly_dark')
sub6.update_annotations(font_size=20)

# % por canal
canais = ['Loja fisica','Loja fisica','Loja fisica','Loja fisica','Instagram','Instagram','Instagram','Anúncios','Anúncios','Recomendação de amigos']
for i in list(vendasfm.index):
    vendasfm.loc[i,'Canal']=random.choice(canais)
c = ['Loja fisica','Instagram','Anúncios','Recomendação de amigos']
v = []
v.append(vendasfm['Canal'].value_counts()['Loja fisica'])
v.append(vendasfm['Canal'].value_counts()['Instagram'])
v.append(vendasfm['Canal'].value_counts()['Anúncios'])
v.append(vendasfm['Canal'].value_counts()['Recomendação de amigos'])
sub6.add_trace(go.Pie(labels=c, values=v, marker=dict(colors=('cyan','royalblue','blue','lightcyan'))), row=1, col=2)
# quais produtos mais contribuíram para o faturamento
x2=[]
y2=[]
pfat = vendasfm[['Produto','Valor Final']].groupby('Produto').sum()
for c in range(0,5):
    x2.append(pfat.idxmax()['Valor Final'])
    y2.append(pfat.max()['Valor Final'])
    for i in list(pfat.index):
        if pfat.loc[i,'Valor Final']==pfat.max()['Valor Final']:
            pfat = pfat.drop(i)
            break
dicp2 = {}
dicp2['Produto']=x2
dicp2['Faturamento']=y2
datap2 = pd.DataFrame(dicp2)
sub6.add_trace(go.Bar(x=list(datap2['Produto']), y=list(datap2['Faturamento']), marker=dict(color=('cyan','royalblue','blue','lightcyan','darkcyan'))), row=1, col=1)
sub6.update_yaxes(title_text='Faturamento', row=1, col=1)

# APP
app =  dash.Dash(__name__)
server = app.server
# INSIDE
app.layout = html.Div(children=[
    html.H1(children='ANÁLISE DE VENDAS (meses: fevereiro x março)'),
    dcc.Graph(id = 'G0', figure = graffat),
    dcc.Graph(id = 'G1', figure = grafluc),
    dcc.Graph(id = 'G2', figure = quantvd),
    dcc.Graph(id = 'G3', figure = sub3),
    dcc.Graph(id = 'G4', figure = sub6),
    dcc.Graph(id = 'G5', figure = top),
    dcc.Graph(id = 'G6', figure = low)
])

# callbacks


# RODANDO
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050)) 
    app.run_server(debug=True, host="0.0.0.0", port=port)
