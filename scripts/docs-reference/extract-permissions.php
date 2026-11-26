<?php
// Every site MCP tool's name, folder group, permission and account-tool flag, in registry order (read-only).
// Run from the in1s application root: OUT=<working folder>/perms.json php <path to this file>
require getcwd().'/vendor/autoload.php';
$app = require getcwd().'/bootstrap/app.php';
$app->make(Illuminate\Contracts\Console\Kernel::class)->bootstrap();

$rows = [];
foreach ((new ReflectionClass(App\Mcp\Servers\SiteServer::class))->getProperty('tools')->getDefaultValue() as $order => $class) {
    $ref = new ReflectionClass($class);
    $name = $ref->getAttributes(Laravel\Mcp\Server\Attributes\Name::class)[0]->newInstance()->value;
    $p = $class::permission();
    $rows[] = [
        'order' => $order,
        'name' => $name,
        'class' => $class,
        'group' => basename(dirname(str_replace(chr(92), '/', $ref->getFileName()))),
        'resource' => $p->resource,
        'action' => $p->action,
        'scope' => $p->scopeArgument,
        'mayPublish' => $p->needsMayPublish,
        'anyMember' => $p->anyMember,
        'account' => in_array($name, App\Mcp\Servers\SiteServer::ACCOUNT_TOOLS, true),
    ];
}

file_put_contents(getenv('OUT'), json_encode($rows, JSON_PRETTY_PRINT));
echo count($rows), " tools\n";
