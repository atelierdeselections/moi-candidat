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

jQuery(document).ready(function() {
 	jQuery('.candidat').each(function() {
		var id_balise=this.id;
		var id_candidat=id_balise.substring(id_balise.lastIndexOf("_")+1,id_balise.length);
		jQuery('#candidat_'+id_candidat).click(function() {
			jQuery('.propositions_candidat').each(function() {
				jQuery(this).css('display','none');
			});	
			jQuery('#proposition_candidat_'+id_candidat).css('display','block');
		});
	});
});

jQuery(document).ready(function() {
 	jQuery('.thematique').each(function() {
		var id_balise=this.id;
		var id_candidat=id_balise.substring(id_balise.lastIndexOf("_")+1,id_balise.length);
		jQuery('#thematique_'+id_candidat).click(function() {
			jQuery('.box_proposition').each(function() {
				jQuery(this).css('display','none');
			});	
			jQuery('.proposition_thematique_'+id_candidat).each(function() {
				jQuery(this).css('display','block');
			});
		});
	});
});


jQuery(document).ready(function() {
		jQuery('#touts_les_candidats').click(function() {
			jQuery('.propositions_candidat').each(function() {
				jQuery(this).css('display','block');
			});
		});
});

jQuery(document).ready(function() {
		jQuery('#toutes_les_thematique').click(function() {
			jQuery('.box_proposition').each(function() {
				jQuery(this).css('display','block');
			});
		});
});
