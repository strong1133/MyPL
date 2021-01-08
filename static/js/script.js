$(document).ready(function () {
    $('#tables-box').empty()
    $('#card_input').empty()

    get_tables();
    get_news();
    active_tab()


})

//Tab
function active_tab() {
    $("div.tab-header div").click(function () {
        const tab_id = $(this).attr("data-tab");

        $("div.tab-header div").removeClass('active')
        $(".tab-content").removeClass('active')

        $(this).addClass('active')
        $("#" + tab_id).addClass('active')
    })
    const tabHeader = document.getElementsByClassName("tab-header")[0];
    const tabIndicator = document.getElementsByClassName("tab-indicator")[0];
    const tabsPane = tabHeader.getElementsByTagName("div");

    for (let i = 0; i < tabsPane.length; i++) {
        tabsPane[i].addEventListener("click", function () {
            tabIndicator.style.left = `calc(calc(100%/4)*${i})`
        });
    }
}

// 순위표 API
function get_tables() {
    $.ajax({
        type: 'GET',
        url: 'api/tables',
        data: {},
        success: function (response) {
            if (response['result'] == 'success') {
                let tables = response['tables']
                for (let i = 0; i < tables.length; i++) {
                    let table = tables[i]

                    makeTable(table['rank'], table['emblem'], table['team_name'], table['played'], table['points'], table['won'], table['draw'], table['lost'], table['gf'], table['ga'], table['gd'])
                }
            }
        }
    })
}

//순위표 append
function makeTable(rank, emblem, team_name, played, points, won, draw, lost, gf, ga, gd) {
    let tempHtml = `<tr>
                    <th scope="row">${rank}</th>
                    <td id="tname"><img src="${emblem}" alt="" id="emblem">
                        ${team_name}</td>
                    <td>${played}</td>
                    <td>${points}</td>
                    <td>${won}</td>
                    <td>${draw}</td>
                    <td>${lost}</td>
                    <td>${gf}</td>
                    <td>${ga}</td>
                    <td>${gd}</td>
                  </tr>`
    $('#tables-box').append(tempHtml)
}

//뉴스 API
function get_news() {
    $.ajax({
        type: 'GET',
        url: 'api/news',
        data: {},
        success: function (response) {
            if (response['result'] == 'success') {
                let newses = response['newses']
                for (let i = 0; i < newses.length; i++) {
                    let news = newses[i]
                    makeNews(news['title'], news['img_url'], news['content'], news['press'], news['post_date'], news['article_url'])
                }
            }
        }
    })
}

//뉴스 append
function makeNews(title, img_url, content, press, post_date, article_url) {
    let tempHtml = `<div class="card">
                        <div class="card-content">
                          <div class="media">
                            <div class="media-left">
                              <figure class="card-image">
                                <img
                                    src="${img_url}"
                                    alt="Placeholder image"
                                />
                              </figure>
                            </div>
                            <div class="media-content">
                              <a href="${article_url}" target="_blank" class="news-title">${title}</a>
                              <p class="subtitle">${content}</p>
                              <p class="press"><img src="${press}" alt=""> <span class="press-date">${post_date}</span></p>
                            </div>
                          </div>
                        </div>
                      </div>`
    $('#card_input').append(tempHtml)
}

