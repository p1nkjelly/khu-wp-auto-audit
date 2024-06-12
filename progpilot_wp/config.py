plugin_path = './plugins'
analysis_file = './analysis.php'
save_path = '../results'
sanitizer_path = './sanitizer.json'
command = f"php {analysis_file} | jq"

code = '''<?php
require_once 'vendor/autoload.php';

$context = new \progpilot\Context;
$analyzer = new \progpilot\Analyzer;

$context->inputs->addSanitizers("{0}");
$context->inputs->setFolder("{1}");
$context->outputs->taintedFlow(TRUE);

$analyzer->run($context);
$results = $context->outputs->getResults();

print_r(json_encode($results));
?>
'''

