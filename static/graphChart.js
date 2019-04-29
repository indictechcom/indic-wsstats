$(function () {

    // Ajax request to get Stats
    $.ajax({
        type: "GET",
        dataType: 'json',
        url: "https://tools.wmflabs.org/indic-wsstats/api/stats",
        crossDomain: true
    })
        .done(function (data) {

            var domains = [];
            var Main_Pages = [];
            var Without_text = [];
            var Proofread = [];
            var Validated = [];

            // Create the array of graph elements
            $.each(data, function (key, value) {
                if (key === "timestamp") {
                    return;
                }
                domains.push(key);
                Main_Pages.push(data[key].Main_Pages);
                Without_text.push(data[key].Without_text);
                Proofread.push(data[key].Proofread);
                Validated.push(data[key].Validated);

            });

            // Create array for background color
            var backgroundColor = [];
            var borderColor = [];
            for (var i in domains) {
                backgroundColor.push("rgba(50,150,200,0.3)");
                borderColor.push("rgba(50,150,200,1)");
            }

            // Function to create the Data Set object
            function CreateDataSet(labels, data) {
                return {
                    labels: labels,
                    datasets: [
                        {
                            data: data,
                            backgroundColor: backgroundColor,
                            borderColor: borderColor,
                            borderWidth: 1
                        }
                    ]
                };
            }

            // Function to create options object
            function CreateOptions(text) {
                return {
                    responsive: true,
                    title: {
                        display: true,
                        position: "top",
                        text: text,
                    },
                    legend: {
                        display: false
                    }
                }
            }

            // Function to create the Bar Chart
            function CreateBar(element, data, options) {
                new Chart(element, {
                    type: "bar",
                    data: data,
                    options: options
                });
            }

            // Select the elements by id
            var mainpage = $("#bar-mainpage");
            var withouttext = $("#bar-withouttext");
            var proofread = $("#bar-proofread");
            var validated = $("#bar-validated");

            // Create the chart
            CreateBar(mainpage, CreateDataSet(domains, Main_Pages), CreateOptions("Total Page Namespace Pages"));
            CreateBar(withouttext, CreateDataSet(domains, Without_text), CreateOptions("Without text"));
            CreateBar(proofread, CreateDataSet(domains, Proofread), CreateOptions("Proofread Pages"));
            CreateBar(validated, CreateDataSet(domains, Validated), CreateOptions("Validated"));

        })
        .fail(function () {

            // If request fails then put error message
            var error = $("<div>").addClass("alert alert-danger").html(
                "<strong>Error!</strong> There is something wrong happen. Please write message to " +
                "<a href=\"https://meta.wikimedia.org/wiki/User:Jayprakash12345\">Jay Prakash</a>."
            );
            $("#graph-charts").empty().append(error);
        });
});