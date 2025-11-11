<?php
/* Smarty version 3.1.48, created on 2025-11-07 18:00:31
  from '/var/www/html/admin989ra7n38/themes/default/template/content.tpl' */

/* @var Smarty_Internal_Template $_smarty_tpl */
if ($_smarty_tpl->_decodeProperties($_smarty_tpl, array (
  'version' => '3.1.48',
  'unifunc' => 'content_690e25afd0dd13_40654445',
  'has_nocache_code' => false,
  'file_dependency' => 
  array (
    '588865734e48b2564ebb2cc222231e94bd8ee560' => 
    array (
      0 => '/var/www/html/admin989ra7n38/themes/default/template/content.tpl',
      1 => 1702485415,
      2 => 'file',
    ),
  ),
  'includes' => 
  array (
  ),
),false)) {
function content_690e25afd0dd13_40654445 (Smarty_Internal_Template $_smarty_tpl) {
?><div id="ajax_confirmation" class="alert alert-success hide"></div>
<div id="ajaxBox" style="display:none"></div>

<div class="row">
	<div class="col-lg-12">
		<?php if ((isset($_smarty_tpl->tpl_vars['content']->value))) {?>
			<?php echo $_smarty_tpl->tpl_vars['content']->value;?>

		<?php }?>
	</div>
</div>
<?php }
}
