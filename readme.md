## 📌 Tutorial: Gerar o JSON de credenciais do Google Console

Para que a aplicação consiga acessar e manipular dados no **Google Sheets**, é necessário criar uma conta de serviço e obter um arquivo de credenciais `.json`.  

---

### 1. Criar um projeto no Google Cloud
1. Acesse [Google Cloud Console](https://console.cloud.google.com/).
2. No canto superior esquerdo, clique em **Selecionar Projeto** → **Novo Projeto**.
3. Dê um nome (ex.: `netline-sheets-app`) e crie.

---

### 2. Ativar a Google Sheets API
1. Com o projeto selecionado, vá em **APIs e Serviços** → **Biblioteca**.
2. Procure por **Google Sheets API**.
3. Clique em **Ativar**.

---

### 3. Criar credenciais
1. Ainda em **APIs e Serviços**, vá em **Credenciais**.
2. Clique em **Criar credenciais** → **Conta de serviço**.
3. Preencha um nome (ex.: `sheets-service-account`).
4. Conclua a criação (os papéis/roles podem ser ignorados ou pode-se usar `Editor` para simplificar).

---

### 4. Gerar chave JSON
1. Abra a conta de serviço criada.
2. Vá na aba **Chaves** → **Adicionar chave** → **Criar nova chave**.
3. Escolha o formato **JSON**.
4. Será feito o download de um arquivo `.json`.  
   👉 Este é o arquivo que deverá ser utilizado no backend da aplicação.

---

### 5. Compartilhar a planilha com a conta de serviço
1. Abra sua planilha no Google Sheets.
2. No canto superior direito, clique em **Compartilhar**.
3. Adicione o **e-mail da conta de serviço** (algo como:  
   `sheets-service-account@seu-projeto.iam.gserviceaccount.com`).
4. Dê permissão de **Editor** (se a aplicação precisar escrever dados).

---

✅ Agora sua aplicação já pode acessar a planilha utilizando as credenciais configuradas.
