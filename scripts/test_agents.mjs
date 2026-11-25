// Offline simulation of the three JavaScript Code nodes.
// No AI calls, network access, or credentials are required.
import assert from "node:assert/strict";
import fs from "node:fs";
import vm from "node:vm";

const path = process.argv[2];
if (!path) throw new Error("Usage: node scripts/test_agents.mjs workflows/<file>.json");
const workflow = JSON.parse(fs.readFileSync(path, "utf8"));
const getNode = (name) => {
  const node = workflow.nodes.find((n) => n.name === name);
  assert.ok(node, "Missing node: " + name);
  assert.equal(node.type, "n8n-nodes-base.code");
  assert.ok(node.parameters?.jsCode);
  return node;
};
function executeCode(name, incoming, previous = {}) {
  const node = getNode(name);
  const context = {
    $input: {
      all: () => incoming.map((json) => ({ json })),
      first: () => ({ json: incoming[0] }),
    },
    $: (nodeName) => ({
      first: () => {
        assert.ok(Object.hasOwn(previous, nodeName), "Missing mock: " + nodeName);
        return { json: previous[nodeName] };
      },
    }),
  };
  const output = vm.runInNewContext(
    "(function () {\n" + node.parameters.jsCode + "\n})()",
    context,
    { timeout: 2000 }
  );
  assert.ok(Array.isArray(output) && output.length > 0 && output[0].json);
  return output[0].json;
}

// Covers normal, duplicate-ID, and malformed-email records.
const users = [
  { id: 1, name: "Ana Exemplo", email: "ana@example.test" },
  { id: 2, name: "Bruno Exemplo", email: "bruno@example.test" },
  { id: 2, name: "Bruno Exemplo", email: "email-invalido" },
];
const prepared = executeCode("Preparar dados para agentes", users);
assert.equal(prepared.quantidade, 3);
assert.equal(prepared.registros.length, 3);
assert.equal(prepared.registros[0].nome, "Ana Exemplo");

const checked = executeCode("Validar dados e indicadores", [prepared]);
const v = checked.validacao;
assert.equal(v.totalRegistros, 3);
assert.equal(v.totalCamposObrigatorios, 9);
assert.equal(v.percentualCompletude, 100);
assert.equal(v.idsDuplicados, 1);
assert.equal(v.emailsFormatoInvalido, 1);
assert.equal(v.emailsSintaxeBasica, 2);
assert.equal(v.aprovacaoHumanaObrigatoria, true);

const previous = {
  "Preparar dados para agentes": prepared,
  "Validar dados e indicadores": checked,
};
for (const [name, label] of [
  ["Agente 1 - Triagem", "Dados examinados"],
  ["Agente 2 - Qualidade", "Qualidade avaliada"],
  ["Agente 3 - Analise", "Indicadores revisados"],
  ["Agente 4 - Relatorio", "Relatorio redigido"],
  ["Agente 5 - Auditoria", "STATUS: APROVACAO_HUMANA_NECESSARIA"],
]) previous[name] = { output: label };

const generated = executeCode("Preparar texto para arquivo", [checked], previous);
assert.ok(typeof generated.relatorio === "string");
for (const title of ["TRIAGEM", "QUALIDADE DOS DADOS", "ANÁLISE DOS DADOS", "RELATÓRIO EXECUTIVO", "AUDITORIA FINAL"]) {
  assert.ok(generated.relatorio.includes(title), "Missing report section " + title);
}
assert.ok(generated.relatorio.includes("APROVACAO_HUMANA_NECESSARIA"));
assert.ok(generated.relatorio.includes("Registros processados: 3"));

assert.throws(
  () => executeCode("Preparar dados para agentes", []),
  /API sem registros/
);
console.log("PASS: preparação, validação determinística, cinco seções e revisão humana (fixtures).");
console.log("NOTE: testes offline NÃO chamam modelos OpenAI e não atestam respostas reais.");
