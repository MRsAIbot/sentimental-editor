$(document).ready(function() {
	$( "#articleForm" ).submit(function( event ) {

		// Stop form from submitting normally
		event.preventDefault();


		// Get some values from elements on the page:
		var $form = $( this ),
			article = $form.find( 'textarea[name="article"]' ).val(),
			title = $form.find('input[name="title"]').val(),
			url = $form.attr( "action" );
	 	
	 	

		// Send the data using post
		var posting = $.post( url, { 'title': title, 'article': article } );

			// Put the results in a div
			posting.done(function( data2 ) {
				data = JSON.parse(data2);

				var text = "";
				var tags = "";
				console.log(data);
				if(data.keywords.length == 0){
					tags = "No keywords found."
				}
				else{
					$.each(data.keywords.sort(function(a, b){return a.sentiment < b.sentiment}), function( key, val ) {
							if(key != 0){
								tags = tags + '<div class="phrases">&nbsp;|&nbsp;<span class="phrase' + val.sentiment + '">' + val.phrase + " </span> </div>";
							}
							else{
								tags = tags + '<div class="phrases"> <span class="phrase' + val.sentiment + '">' + val.phrase + " </span> </div> ";
							}
						
					});
					
					
				}
				$(".phrases").remove();
				$("#keywords").append(tags);

				text = text + '<div class="tweets">';
				if(data.tweets.length == 0){
					text = text + "No tweets found."
				}
				else{
					for(var j=0; j< data.tweets.length; j++){
								var tweet = data.tweets[j];
								text = text +  '<div class="bar' + tweet.sentiment + '"></div>' + '<div class="created">' + tweet.created + '</div> <div class="image"><img src="' + tweet.profile_image + '">'+ '</div> <div class="name">' + tweet.name + '</div> <div class="username"> @' + tweet.user + '</div>' + '<div class="content"> <br>' + tweet.text + '</div> <br> <hr>' ;
								if(j==4){
									break;
								}
							}
					
				}
				text = text + "</div>";
				$(".tweets").remove();
				$( "#twitter" ).append(text);
			});

	});


});