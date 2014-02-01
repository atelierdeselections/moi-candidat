jQuery(document).ready(function() {
 	jQuery('.description_proposition').each(function(i) {
 		jQuery('#plus_'+i).click(function() {
 			if (jQuery('#description_proposition_'+i).css('display') == 'none') {
 				jQuery('#description_proposition_'+i).show('medium');
 				jQuery('.description_proposition').each(function(j) {
					if (i!=j){	
						jQuery('#description_proposition_'+j).hide('medium');
					}
				});
			} else {
				jQuery('#description_proposition_'+i).hide('medium');
			}
		});
	});
});