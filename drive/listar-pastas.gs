/**
 * Gera um CSV ligando cada coleta à sua pasta de fotos no Google Drive.
 * Só é necessário se você quiser links diretos — sem isso, o app já acha as
 * fotos procurando pelo código no Drive (o botão 🔍 de cada coleta).
 *
 * Como usar:
 *   1. Abra a pasta "Specimens" no Drive e copie o id da URL:
 *      drive.google.com/drive/folders/ESTE_TRECHO_AQUI
 *   2. Vá em script.google.com → Novo projeto → cole este arquivo inteiro.
 *   3. Troque ID_DA_PASTA abaixo pelo id copiado.
 *   4. Executar → autorize o acesso ao seu Drive (é o seu próprio script).
 *   5. O arquivo "pastas-fotos.csv" aparece na raiz do seu Drive. Baixe.
 *   6. No app: aba Coletas → Importar planilha → escolha o CSV →
 *      em "Modo", selecione "Completar registros existentes (casar pelo código)".
 *
 * Pastas com sufixo (TAJ102A, TAJ102B) não casam com nenhum registro e vão
 * aparecer como "não encontrados" — tudo bem: para essas coletas o botão 🔍
 * continua funcionando e mostra todas as subpastas de uma vez.
 */
function gerarCSV() {
  var ID_DA_PASTA = "COLE_O_ID_AQUI";

  var raiz = DriveApp.getFolderById(ID_DA_PASTA);
  var pastas = raiz.getFolders();
  var linhas = ['"Coleta";"Pasta de fotos"'];
  var total = 0;

  while (pastas.hasNext()) {
    var pasta = pastas.next();
    var nome = pasta.getName().trim();
    if (!/\d/.test(nome)) continue;              // ignora "pending" e afins
    var url = "https://drive.google.com/drive/folders/" + pasta.getId();
    linhas.push('"' + nome.replace(/"/g, '""') + '";"' + url + '"');
    total++;
  }

  var csv = "﻿" + linhas.join("\r\n");
  var antigos = DriveApp.getFilesByName("pastas-fotos.csv");
  while (antigos.hasNext()) antigos.next().setTrashed(true);
  DriveApp.createFile("pastas-fotos.csv", csv, MimeType.CSV);

  Logger.log(total + " pastas exportadas para pastas-fotos.csv");
}
