# Backend no Firebase (Google Cloud)

Substitui o Supabase, que pausa projetos gratuitos após ~1 semana sem uso.
O Firebase **não pausa por inatividade** e, no volume deste app, custa **US$ 0**.

## Configuração (tudo pelo navegador, ~5 min)

1. **Criar o projeto** — [console.firebase.google.com](https://console.firebase.google.com)
   → "Criar projeto". Pode desativar o Google Analytics.

2. **Ativar o login por e-mail** — Build → Authentication → "Vamos começar"
   → Sign-in method → **E-mail/senha** → ativar → Salvar.

3. **Criar sua conta** — Authentication → aba Users → "Adicionar usuário"
   → seu e-mail + senha.

4. **Fechar o cadastro** (só você deve ter conta) — Authentication → Settings
   → User actions → desmarcar **"Enable create (sign-up)"** → Salvar.

5. **Criar o banco** — Build → Firestore Database → "Criar banco de dados"
   → região `southamerica-east1` (São Paulo) → começar em **modo produção**.

6. **Publicar as regras** — Firestore Database → aba **Regras** → colar o conteúdo
   de [`firestore.rules`](firestore.rules) → Publicar.

7. **Pegar as credenciais** — ⚙ Configurações do projeto → aba Geral
   → role até "Seus apps" → se não houver nenhum, clique no ícone `</>` (Web)
   e registre um app (sem hospedagem). Copie `apiKey` e `projectId`.

8. **Ligar no app** — em `index.html`, preencha:

   ```js
   const FIREBASE = {
     apiKey: "AIza...",
     projectId: "phd-tracker-xxxxx",
   };
   ```

   O Firebase tem prioridade sobre o Supabase: assim que esses dois campos
   estiverem preenchidos, o app passa a usar o Google Cloud.

## Migrar os dados do Supabase

1. Abra o app **ainda no Supabase** e clique em **Exportar** (baixa um `.json`).
   Se o projeto Supabase estiver pausado, use um dispositivo que já tenha os dados
   em cache: entre em "Continuar offline" e exporte dali.
2. Preencha o bloco `FIREBASE` e publique.
3. Abra o app, entre com a conta nova e clique em **Importar**, escolhendo o `.json`.
4. Confira o selo "☁ salvo" no cabeçalho e abra em outro dispositivo para validar.

## Sobre a chave `apiKey`

Ela é **pública por natureza** (aparece no HTML de qualquer app Firebase) e não dá
acesso a nada sozinha: a segurança vem das regras acima + da sua senha. Não confunda
com uma chave de serviço, essa sim secreta e que não é usada aqui.

## Custos

Plano **Spark** (gratuito, sem cartão): 1 GiB de armazenamento, 50 mil leituras e
20 mil gravações por dia, autenticação ilimitada por e-mail/senha. Este app faz
cerca de 1 leitura ao abrir e 1 gravação por edição — algumas centenas por dia no
uso mais intenso. Fica dentro do gratuito com folga, sem consumir créditos.

Limite técnico: cada documento do Firestore aceita 1 MiB. Todo o estado do app é
gravado num documento só; o app avisa no cabeçalho se passar de 900 KB (hoje, com
~220 coletas, o arquivo tem cerca de 150 KB).
