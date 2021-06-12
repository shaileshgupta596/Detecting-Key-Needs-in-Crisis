	var search_box = document.getElementById("search_box");
	var search_error = document.getElementById("search_error");
	var search_btn = document.getElementById("search_btn");
	
	console.log("entered");
	search_box.addEventListener("input",function()
	{
		console.log("Changed");
		
		if(this.value[this.value.length-1]==" ")
		{
			this.value = this.value.slice(0,this.value.length-1);
			search_error.innerText = "No space!! "
			search_error.style.display="inline";
			/*search_btn.setAttribute("disabled", "disabled");*/
		}
		else if(this.value.length==0)
		{
			search_error.innerText = "Please type something!"
			search_error.style.display="inline";
			search_btn.setAttribute("disabled", "disabled");
			
		}
		else
		{
			search_error.style.display="none";
			search_btn.removeAttribute("disabled")
		}
	});


	search_btn.addEventListener("click", function(event)
	{
		console.log("Button clicked");
		
	});