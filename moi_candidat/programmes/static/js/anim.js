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
			jQuery('.candidat').css('background','#EEEEEE')
			jQuery('.propositions_candidat').each(function() {
				jQuery(this).css('display','none');
			});	
			jQuery('#'+id_balise).css('background','#CCCCCC');
			jQuery('#proposition_candidat_'+id_candidat).css('display','block');
		});
	});
});

jQuery(document).ready(function() {
 	jQuery('.thematique').each(function() {
		var id_balise=this.id;
		var id_candidat=id_balise.substring(id_balise.lastIndexOf("_")+1,id_balise.length);
		jQuery('#thematique_'+id_candidat).click(function() {
			jQuery('.thematique').css('background','#252A3A');
			jQuery('#toutes_les_thematique').css('background','#252A3A');
			jQuery('.box_proposition').each(function() {
				jQuery(this).css('display','none');	
			});	
			jQuery('.proposition_thematique_'+id_candidat).each(function() {
				jQuery('#'+id_balise).css('background','#353A4A');
				jQuery(this).css('display','block');
			});
		});
	});
});


jQuery(document).ready(function() {
		jQuery('#touts_les_candidats').click(function() {
			jQuery('.candidat').css('background','#EEEEEE');
			jQuery('#touts_les_candidats').css('background','#CCCCCC');
			jQuery('.propositions_candidat').each(function() {
				jQuery(this).css('display','block');
			});
		});
});

jQuery(document).ready(function() {
		jQuery('#toutes_les_thematique').click(function() {
			jQuery('.thematique').css('background','#252A3A');
			jQuery('#toutes_les_thematique').css('background','#353A4A');
			jQuery('.box_proposition').each(function() {
				jQuery(this).css('display','block');
			});
		});
});
