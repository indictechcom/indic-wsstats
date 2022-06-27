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
            var PageNamescpacePages = [];
            var Without_text = [];
            var NotProofread = [];
            var Problematic = [];
            var Proofread = [];
            var Validated = [];
            var Main_Pages = [];
            var With_scans = [];
            var Without_scans = [];

            var proofreadPercentage = [];
            var transcludedPercentage = [];

            // Array for Average page size
            var Main_APG = [];
            var Page_APS = [];

            // Create the array of graph elements
            $.each(data, function (key, value) {
                if (key === "timestamp") {
                    return;
                }
                domains.push(key);
                PageNamescpacePages.push(data[key].Num_of_pages);
                Without_text.push(data[key].Without_text);
                NotProofread.push(data[key].Not_proofread);
                Problematic.push(data[key].Problematic);
                Proofread.push(data[key].Proofread);
                Validated.push(data[key].Validated);
                Main_Pages.push(data[key].Main_Pages);
                With_scans.push(data[key].Main_WithScan);
                Without_scans.push(data[key].Main_WithOutScan);

                proofreadPercentage.push(Math.round(100 * ((100 * data[key].Proofread / data[key].Num_of_pages))) / 100);
                transcludedPercentage.push(Math.round(100 * (100 * data[key].Main_WithScan / (data[key].Main_WithScan + data[key].Main_WithOutScan))) / 100);

                Main_APG.push(data[key].Main_APS);
                Page_APS.push(data[key].Page_APS);
            });

            // Create array for background color
            var backgroundColor = [];
            var borderColor = [];
            for (var i in domains) {
                backgroundColor.push("rgba(50,150,200,0.3)");
                borderColor.push("rgba(50,150,200,1)");
            }

            // Function to create the Data Set object
            function CreateDataSet(labels, data, dataset_label) {
                return {
                    labels: labels,
                    datasets: [
                        {
                            data: data,
                            label: dataset_label,
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
            var proofreadper = $("#bar-proofreadper");
            var transcludedper = $("#bar-transcludedper");

            var pagenamespace = $("#bar-pagenamespace");
            var withouttext = $("#bar-withouttext");
            var notproofread = $("#bar-notproofread");
            var problematic = $("#bar-problematic");
            var proofread = $("#bar-proofread");
            var validated = $("#bar-validated");

            var mainpage = $("#bar-mainpage");
            var withscan = $("#bar-withscan");
            var withoutscan = $("#bar-withoutscan");

            var main_apg = $("#bar-main-aps");
            var page_aps = $("#bar-page-aps");
            
            // // Create the average page size chart
            // CreateBar(main_apg, CreateDataSet(domains, Main_APG, ""), CreateOptions('uttfytffuf'));
            // CreateBar(page_aps, CreateDataSet(domains, Page_APS, ""), CreateOptions(_('page-ns-opts')));

            // // Create the percentage chart
            // CreateBar(proofreadper, CreateDataSet(domains, proofreadPercentage, ""), CreateOptions(_('proofread') + " %"));
            // CreateBar(transcludedper, CreateDataSet(domains, transcludedPercentage, ""), CreateOptions(_('transclude') + " %"));

            // // Create the page namespace chart
            // CreateBar(pagenamespace, CreateDataSet(domains, PageNamescpacePages, ""), CreateOptions(_('tot-pages')));
            // CreateBar(withouttext, CreateDataSet(domains, Without_text, ""), CreateOptions(_('no-text')));
            // CreateBar(notproofread, CreateDataSet(domains, NotProofread, ""), CreateOptions(_('not-proofread')));
            // CreateBar(problematic, CreateDataSet(domains, Problematic, ""), CreateOptions(_('problem')));
            // CreateBar(proofread, CreateDataSet(domains, Proofread, ""), CreateOptions(_('proofread-pgs')));
            // CreateBar(validated, CreateDataSet(domains, Validated, ""), CreateOptions(_('valid')));

            // // Create the main namespace chart
            // CreateBar(mainpage, CreateDataSet(domains, Main_Pages), CreateOptions(_('tot-pages')));
            // CreateBar(withscan, CreateDataSet(domains, With_scans), CreateOptions(_('scan')));
            // CreateBar(withoutscan, CreateDataSet(domains, Without_scans), CreateOptions(_('no-scan')));

        })
        .fail(function () {

            // If request fails then put error message
            var error = $("<div>").addClass("alert alert-danger").html(
                "<strong>Error!</strong> There is something wrong happen. Please write message to " +
                "<a href=\"https://meta.wikimedia.org/wiki/Indic-TechCom/Requests\">Indic-TechCom/Requests</a>."
            );
            $("#graph-charts").empty().append(error);
        });
});