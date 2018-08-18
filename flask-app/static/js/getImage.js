function check_progress(job_id) {
    function worker() {
        $.get('status/' + job_id, function(data) {
            if (data.status === 201 || data.status === 202) {
                setTimeout(worker, 1000)
            } else if (data.status === 200) {
                console.log(data); // success
            } else {
                console.log(data); // error
            }
        })
    }
}