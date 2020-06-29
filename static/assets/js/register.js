$(document).ready(function() {
//On click signup, hide login and show registration form
	$("#signup").click(function() {
		$("#first").slideUp("slow", function(){
			$("#second").slideDown("slow");
		});
	});

	//On click signup, hide registration and show login form
	$("#signin").click(function() {
		$("#second").slideUp("slow", function(){
			$("#first").slideDown("slow");
		});
	});

});

	//Toast for Success message with title
	function showSuccessToastWithTitle(msg, title, type) {
		editTypeAndTime(type)
		toastr.success(msg, title)
	}

	function showWarningToastWithTitle(msg, title, type) {
		editTypeAndTime(type)
		toastr.warning(msg, title)
	}

	function  showErrorToastWithTitle(msg, title, type) {
		editTypeAndTime(type)
		 toastr.error(msg, title);
	}

	function  showInfoToastWithTitle(msg, title, type) {
		editTypeAndTime(type)
		 toastr.info(msg, title);
	}

//for configuration edit of toaster
const editTypeAndTime = function(type) {
	toastr.options.positionClass = type
	toastr.options.extendedTimeOut = 0;
	toastr.options.timeOut = 10000;
	toastr.options.fadeOut = 1000000;
	toastr.options.fadeIn = 0;
	toastr.options.preventDuplicates = true;
	toastr.options.progressBar = true;
	toastr.options.rtl = true;

};
