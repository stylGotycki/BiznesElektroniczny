<?php
/* Smarty version 3.1.48, created on 2025-11-07 18:00:37
  from '/var/www/html/modules/welcome/views/templates/lost.tpl' */

/* @var Smarty_Internal_Template $_smarty_tpl */
if ($_smarty_tpl->_decodeProperties($_smarty_tpl, array (
  'version' => '3.1.48',
  'unifunc' => 'content_690e25b5149ca7_23842288',
  'has_nocache_code' => false,
  'file_dependency' => 
  array (
    '40409c48066d4d283adcead3db93a109c00c6a11' => 
    array (
      0 => '/var/www/html/modules/welcome/views/templates/lost.tpl',
      1 => 1676360366,
      2 => 'file',
    ),
  ),
  'includes' => 
  array (
  ),
),false)) {
function content_690e25b5149ca7_23842288 (Smarty_Internal_Template $_smarty_tpl) {
?>
<div class="onboarding onboarding-popup bootstrap">
  <div class="content">
    <p><?php echo call_user_func_array( $_smarty_tpl->smarty->registered_plugins[Smarty::PLUGIN_FUNCTION]['l'][0], array( array('s'=>'Hey! Are you lost?','d'=>'Modules.Welcome.Admin'),$_smarty_tpl ) );?>
</p>
    <p><?php echo call_user_func_array( $_smarty_tpl->smarty->registered_plugins[Smarty::PLUGIN_FUNCTION]['l'][0], array( array('s'=>'To continue, click here:','d'=>'Modules.Welcome.Admin'),$_smarty_tpl ) );?>
</p>
    <div class="text-center">
      <button class="btn btn-primary onboarding-button-goto-current"><?php echo call_user_func_array( $_smarty_tpl->smarty->registered_plugins[Smarty::PLUGIN_FUNCTION]['l'][0], array( array('s'=>'Continue','d'=>'Modules.Welcome.Admin'),$_smarty_tpl ) );?>
</button>
    </div>
    <p><?php echo call_user_func_array( $_smarty_tpl->smarty->registered_plugins[Smarty::PLUGIN_FUNCTION]['l'][0], array( array('s'=>'If you want to stop the tutorial for good, click here:','d'=>'Modules.Welcome.Admin'),$_smarty_tpl ) );?>
</p>
    <div class="text-center">
      <button class="btn btn-alert onboarding-button-stop"><?php echo call_user_func_array( $_smarty_tpl->smarty->registered_plugins[Smarty::PLUGIN_FUNCTION]['l'][0], array( array('s'=>'Quit the Welcome tutorial','d'=>'Modules.Welcome.Admin'),$_smarty_tpl ) );?>
</button>
    </div>
  </div>
</div>
<?php }
}
