import re

def normalize_spaces(text):
    return re.sub(r'\s{2,}', ' ', text)

print(normalize_spaces("""
                       <div class="Box-sc-g0xbh4-0 JcuiZ">
                                                        <div data-hpc="true" class="Box-sc-g0xbh4-0 iKysQH">
                                                            <div data-testid="results-list"
                                                                class="Box-sc-g0xbh4-0 gZKkEq">
                                                                <div class="Box-sc-g0xbh4-0 flszRz">
                                                                    <div class="Box-sc-g0xbh4-0 cSURfY">
                                                                        <div class="Box-sc-g0xbh4-0 gPrlij">
                                                                            <h3 class="Box-sc-g0xbh4-0 cvnppv">
                                                                                <div class="Box-sc-g0xbh4-0 kYLlPM">
                                                                                    <div class="Box-sc-g0xbh4-0 eurdCD">
                                                                                        <img data-component="Avatar" class="prc-Avatar-Avatar-ZRS-m" alt="" width="20" height="20" style="--avatarSize-regular:20px" src="https://github.com/ValkA.png?size=40" data-testid="github-avatar"/>
                                                                                    </div>
                                                                                    <div
                                                                                        class="Box-sc-g0xbh4-0 MHoGG search-title">
                                                                                        <a class="prc-Link-Link-85e08"
                                                                                            href="/ValkA/BraceletIOT"><span class="Box-sc-g0xbh4-0 kzfhBO search-match prc-Text-Text-0ima0">ValkA/Bracelet<em>IOT</em></span></a>
                                                                                    </div>
                                                                                </div>
                                                                            </h3>
                                                                            <div class="Box-sc-g0xbh4-0 dcdlju">
                                                                                <span class="Box-sc-g0xbh4-0 gKFdvh search-match prc-Text-Text-0ima0">A POC of smart arduino bracelet for Medical Corps that is attached to an injured person in order to record meidcal events </span>
                                                                            </div>
                                                                            <div class="Box-sc-g0xbh4-0 jgRnBg">
                                                                                <div><a class="Box-sc-g0xbh4-0 hgRXpf prc-Link-Link-85e08"
                                                                                        href="/topics/iot">iot</a></div>
                                                                                <div><a class="Box-sc-g0xbh4-0 hgRXpf prc-Link-Link-85e08"
                                                                                        href="/topics/arduino">arduino</a>
                                                                                </div>
                                                                                <div><a class="Box-sc-g0xbh4-0 hgRXpf prc-Link-Link-85e08"
                                                                                        href="/topics/medicine">medicine</a>
                                                                                </div>
                                                                                <div><a class="Box-sc-g0xbh4-0 hgRXpf prc-Link-Link-85e08"
                                                                                        href="/topics/serial">serial</a>
                                                                                </div>
                                                                                <div><a class="Box-sc-g0xbh4-0 hgRXpf prc-Link-Link-85e08"
                                                                                        href="/topics/bluetooth">bluetooth</a>
                                                                                </div>
                                                                            </div>
                                                                            <ul class="Box-sc-g0xbh4-0 bZkODq">
                                                                                <li class="Box-sc-g0xbh4-0 iyzdzM">
                                                                                    <div class="Box-sc-g0xbh4-0 hjDqIa">
                                                                                        <div
                                                                                            class="Box-sc-g0xbh4-0 eMVVfe">
                                                                                        </div>
                                                                                    </div>
                                                                                    <span aria-label="C++ language">C++</span>
                                                                                </li>
                                                                                <span class="Box-sc-g0xbh4-0 ifbKcf prc-Text-Text-0ima0" aria-hidden="true">·</span>
                                                                                <li class="Box-sc-g0xbh4-0 iyzdzM"><a
                                                                                        class="Box-sc-g0xbh4-0 jJYFGF prc-Link-Link-85e08"
                                                                                        href="/ValkA/BraceletIOT/stargazers"
                                                                                        aria-label="12 stars"><svg
                                                                                            aria-hidden="true"
                                                                                            focusable="false"
                                                                                            class="octicon octicon-star Octicon-sc-9kayk9-0 kPmFhj"
                                                                                            viewBox="0 0 16 16"
                                                                                            width="16" height="16"
                                                                                            fill="currentColor"
                                                                                            display="inline-block"
                                                                                            overflow="visible"
                                                                                            style="vertical-align:text-bottom">
                                                                                            <path
                                                                                                d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.751.751 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Zm0 2.445L6.615 5.5a.75.75 0 0 1-.564.41l-3.097.45 2.24 2.184a.75.75 0 0 1 .216.664l-.528 3.084 2.769-1.456a.75.75 0 0 1 .698 0l2.77 1.456-.53-3.084a.75.75 0 0 1 .216-.664l2.24-2.183-3.096-.45a.75.75 0 0 1-.564-.41L8 2.694Z">
                                                                                            </path>
                                                                                        </svg><span class="prc-Text-Text-0ima0">12</span></a>
                                                                                </li>
                                                                                <span class="Box-sc-g0xbh4-0 ifbKcf prc-Text-Text-0ima0" aria-hidden="true">·</span>
                                                                                <li class="Box-sc-g0xbh4-0 iyzdzM">
                                                                                    <span>Updated <div title="Jun 21, 2018, 8:42 AM UTC" class="Truncate__StyledTruncate-sc-23o1d2-0 liVpTx"><span class="prc-Text-Text-0ima0" title="Jun 21, 2018, 8:42 AM UTC">on Jun 21, 2018</span>
                                                                        </div></span></li>
                                                                        </ul>
                                                                    </div>
                                                                    <div class="Box-sc-g0xbh4-0 gtlRHe">
                                                                        <div class="Box-sc-g0xbh4-0 fvaNTI"><a
                                                                                type="button"
                                                                                href="/login?return_to=https%3A%2F%2Fgithub.com%2Fsearch%3Fq%3Diot%2520wearable%26type%3Drepositories%26p%3D2"
                                                                                class="prc-Button-ButtonBase-c50BI"
                                                                                data-loading="false" data-size="small"
                                                                                data-variant="default"
                                                                                aria-describedby=":R1goqjb:-loading-announcement"><span data-component="buttonContent" data-align="center" class="prc-Button-ButtonContent-HKbr-"><span data-component="leadingVisual" class="prc-Button-Visual-2epfX prc-Button-VisualWrap-Db-eB"><svg aria-hidden="true" focusable="false" class="octicon octicon-star" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.751.751 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Zm0 2.445L6.615 5.5a.75.75 0 0 1-.564.41l-3.097.45 2.24 2.184a.75.75 0 0 1 .216.664l-.528 3.084 2.769-1.456a.75.75 0 0 1 .698 0l2.77 1.456-.53-3.084a.75.75 0 0 1 .216-.664l2.24-2.183-3.096-.45a.75.75 0 0 1-.564-.41L8 2.694Z"></path></svg></span><span data-component="text" class="prc-Button-Label-pTQ3x">Star</span></span></a>
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <div class="Box-sc-g0xbh4-0 flszRz">
                                                                <div class="Box-sc-g0xbh4-0 cSURfY">
                                                                    <div class="Box-sc-g0xbh4-0 gPrlij">
                                                                        <h3 class="Box-sc-g0xbh4-0 cvnppv">
                                                                            <div class="Box-sc-g0xbh4-0 kYLlPM">
                                                                                <div class="Box-sc-g0xbh4-0 eurdCD"><img data-component="Avatar" class="prc-Avatar-Avatar-ZRS-m" alt="" width="20" height="20" style="--avatarSize-regular:20px" src="https://github.com/subham9777.png?size=40" data-testid="github-avatar"/>
                                                                                </div>
                                                                                <div
                                                                                    class="Box-sc-g0xbh4-0 MHoGG search-title">
                                                                                    <a class="prc-Link-Link-85e08"
                                                                                        href="/subham9777/Prediction-of-Tool-Wear"><span class="Box-sc-g0xbh4-0 kzfhBO search-match prc-Text-Text-0ima0">subham9777/Prediction-of-Tool-Wear</span></a>
                                                                                </div>
                                                                            </div>
                                                                        </h3>
                                                                        <div class="Box-sc-g0xbh4-0 dcdlju">
                                                                            <span class="Box-sc-g0xbh4-0 gKFdvh search-match prc-Text-Text-0ima0"><em>IoT</em> based Tool <em>Wear</em> Prediction, a project to collect and analyze vibration data in MATLAB and use the data to predict for tool <em>wear</em>. </span>
                                                                        </div>
                                                                        <ul class="Box-sc-g0xbh4-0 bZkODq">
                                                                            <li class="Box-sc-g0xbh4-0 iyzdzM">
                                                                                <div class="Box-sc-g0xbh4-0 hjDqIa">
                                                                                    <div class="Box-sc-g0xbh4-0 ekXZBT">
                                                                                    </div>
                                                                                </div>
                                                                                <span aria-label="MATLAB language">MATLAB</span>
                                                                            </li>
                                                                            <span class="Box-sc-g0xbh4-0 ifbKcf prc-Text-Text-0ima0" aria-hidden="true">·</span>
                                                                            <li class="Box-sc-g0xbh4-0 iyzdzM"><a
                                                                                    class="Box-sc-g0xbh4-0 jJYFGF prc-Link-Link-85e08"
                                                                                    href="/subham9777/Prediction-of-Tool-Wear/stargazers"
                                                                                    aria-label="8 stars"><svg
                                                                                        aria-hidden="true"
                                                                                        focusable="false"
                                                                                        class="octicon octicon-star Octicon-sc-9kayk9-0 kPmFhj"
                                                                                        viewBox="0 0 16 16" width="16"
                                                                                        height="16" fill="currentColor"
                                                                                        display="inline-block"
                                                                                        overflow="visible"
                                                                                        style="vertical-align:text-bottom">
                                                                                        <path
                                                                                            d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.751.751 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Zm0 2.445L6.615 5.5a.75.75 0 0 1-.564.41l-3.097.45 2.24 2.184a.75.75 0 0 1 .216.664l-.528 3.084 2.769-1.456a.75.75 0 0 1 .698 0l2.77 1.456-.53-3.084a.75.75 0 0 1 .216-.664l2.24-2.183-3.096-.45a.75.75 0 0 1-.564-.41L8 2.694Z">
                                                                                        </path>
                                                                                    </svg><span class="prc-Text-Text-0ima0">8</span></a>
                                                                            </li>
                                                                            <span class="Box-sc-g0xbh4-0 ifbKcf prc-Text-Text-0ima0" aria-hidden="true">·</span>
                                                                            <li class="Box-sc-g0xbh4-0 iyzdzM">
                                                                                <span>Updated <div title="Jun 21, 2020, 8:35 AM UTC" class="Truncate__StyledTruncate-sc-23o1d2-0 liVpTx"><span class="prc-Text-Text-0ima0" title="Jun 21, 2020, 8:35 AM UTC">on Jun 21, 2020</span>
                                                                    </div></span></li>
                                                                    </ul>
                                                                </div>
                                                                <div class="Box-sc-g0xbh4-0 gtlRHe">
                                                                    <div class="Box-sc-g0xbh4-0 fvaNTI"><a type="button"
                                                                            href="/login?return_to=https%3A%2F%2Fgithub.com%2Fsearch%3Fq%3Diot%2520wearable%26type%3Drepositories%26p%3D2"
                                                                            class="prc-Button-ButtonBase-c50BI"
                                                                            data-loading="false" data-size="small"
                                                                            data-variant="default"
                                                                            aria-describedby=":R1h8qjb:-loading-announcement"><span data-component="buttonContent" data-align="center" class="prc-Button-ButtonContent-HKbr-"><span data-component="leadingVisual" class="prc-Button-Visual-2epfX prc-Button-VisualWrap-Db-eB"><svg aria-hidden="true" focusable="false" class="octicon octicon-star" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.751.751 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Zm0 2.445L6.615 5.5a.75.75 0 0 1-.564.41l-3.097.45 2.24 2.184a.75.75 0 0 1 .216.664l-.528 3.084 2.769-1.456a.75.75 0 0 1 .698 0l2.77 1.456-.53-3.084a.75.75 0 0 1 .216-.664l2.24-2.183-3.096-.45a.75.75 0 0 1-.564-.41L8 2.694Z"></path></svg></span><span data-component="text" class="prc-Button-Label-pTQ3x">Star</span></span></a>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                        </div>
                                                        <div class="Box-sc-g0xbh4-0 flszRz">
                                                            <div class="Box-sc-g0xbh4-0 cSURfY">
                                                                <div class="Box-sc-g0xbh4-0 gPrlij">
                                                                    <h3 class="Box-sc-g0xbh4-0 cvnppv">
                                                                        <div class="Box-sc-g0xbh4-0 kYLlPM">
                                                                            <div class="Box-sc-g0xbh4-0 eurdCD"><img data-component="Avatar" class="prc-Avatar-Avatar-ZRS-m" alt="" width="20" height="20" style="--avatarSize-regular:20px" src="https://github.com/javidsheik.png?size=40" data-testid="github-avatar"/>
                                                                            </div>
                                                                            <div
                                                                                class="Box-sc-g0xbh4-0 MHoGG search-title">
                                                                                <a class="prc-Link-Link-85e08"
                                                                                    href="/javidsheik/wear-fitness"><span class="Box-sc-g0xbh4-0 kzfhBO search-match prc-Text-Text-0ima0">javidsheik/wear-fitness</span></a>
                                                                            </div>
                                                                        </div>
                                                                    </h3>
                                                                    <div class="Box-sc-g0xbh4-0 dcdlju">
                                                                        <span class="Box-sc-g0xbh4-0 gKFdvh search-match prc-Text-Text-0ima0"><em>iot</em> - <em>wearables</em> - fitness </span>
                                                                    </div>
                                                                    <ul class="Box-sc-g0xbh4-0 bZkODq">
                                                                        <li class="Box-sc-g0xbh4-0 iyzdzM">
                                                                            <div class="Box-sc-g0xbh4-0 hjDqIa">
                                                                                <div class="Box-sc-g0xbh4-0 jdPrcA">
                                                                                </div>
                                                                            </div>
                                                                            <span aria-label="Objective-C language">Objective-C</span>
                                                                        </li>
                                                                        <span class="Box-sc-g0xbh4-0 ifbKcf prc-Text-Text-0ima0" aria-hidden="true">·</span>
                                                                        <li class="Box-sc-g0xbh4-0 iyzdzM"><a
                                                                                class="Box-sc-g0xbh4-0 jJYFGF prc-Link-Link-85e08"
                                                                                href="/javidsheik/wear-fitness/stargazers"
                                                                                aria-label="2 stars"><svg
                                                                                    aria-hidden="true" focusable="false"
                                                                                    class="octicon octicon-star Octicon-sc-9kayk9-0 kPmFhj"
                                                                                    viewBox="0 0 16 16" width="16"
                                                                                    height="16" fill="currentColor"
                                                                                    display="inline-block"
                                                                                    overflow="visible"
                                                                                    style="vertical-align:text-bottom">
                                                                                    <path
                                                                                        d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.751.751 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Zm0 2.445L6.615 5.5a.75.75 0 0 1-.564.41l-3.097.45 2.24 2.184a.75.75 0 0 1 .216.664l-.528 3.084 2.769-1.456a.75.75 0 0 1 .698 0l2.77 1.456-.53-3.084a.75.75 0 0 1 .216-.664l2.24-2.183-3.096-.45a.75.75 0 0 1-.564-.41L8 2.694Z">
                                                                                    </path>
                                                                                </svg><span class="prc-Text-Text-0ima0">2</span></a>
                                                                        </li>
                                                                        <span class="Box-sc-g0xbh4-0 ifbKcf prc-Text-Text-0ima0" aria-hidden="true">·</span>
                                                                        <li class="Box-sc-g0xbh4-0 iyzdzM">
                                                                            <span>Updated <div title="Jan 15, 2015, 6:16 PM UTC" class="Truncate__StyledTruncate-sc-23o1d2-0 liVpTx"><span class="prc-Text-Text-0ima0" title="Jan 15, 2015, 6:16 PM UTC">on Jan 15, 2015</span>
                                                                </div></span></li>
                                                                </ul>
                                                            </div>
                                                            <div class="Box-sc-g0xbh4-0 gtlRHe">
                                                                <div class="Box-sc-g0xbh4-0 fvaNTI"><a type="button"
                                                                        href="/login?return_to=https%3A%2F%2Fgithub.com%2Fsearch%3Fq%3Diot%2520wearable%26type%3Drepositories%26p%3D2"
                                                                        class="prc-Button-ButtonBase-c50BI"
                                                                        data-loading="false" data-size="small"
                                                                        data-variant="default"
                                                                        aria-describedby=":R1hoqjb:-loading-announcement"><span data-component="buttonContent" data-align="center" class="prc-Button-ButtonContent-HKbr-"><span data-component="leadingVisual" class="prc-Button-Visual-2epfX prc-Button-VisualWrap-Db-eB"><svg aria-hidden="true" focusable="false" class="octicon octicon-star" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.751.751 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Zm0 2.445L6.615 5.5a.75.75 0 0 1-.564.41l-3.097.45 2.24 2.184a.75.75 0 0 1 .216.664l-.528 3.084 2.769-1.456a.75.75 0 0 1 .698 0l2.77 1.456-.53-3.084a.75.75 0 0 1 .216-.664l2.24-2.183-3.096-.45a.75.75 0 0 1-.564-.41L8 2.694Z"></path></svg></span><span data-component="text" class="prc-Button-Label-pTQ3x">Star</span></span></a>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div class="Box-sc-g0xbh4-0 flszRz">
                                                        <div class="Box-sc-g0xbh4-0 cSURfY">
                                                            <div class="Box-sc-g0xbh4-0 gPrlij">
                                                                <h3 class="Box-sc-g0xbh4-0 cvnppv">
                                                                    <div class="Box-sc-g0xbh4-0 kYLlPM">
                                                                        <div class="Box-sc-g0xbh4-0 eurdCD"><img data-component="Avatar" class="prc-Avatar-Avatar-ZRS-m" alt="" width="20" height="20" style="--avatarSize-regular:20px" src="https://github.com/StuartIanNaylor.png?size=40" data-testid="github-avatar"/>
                                                                        </div>
                                                                        <div class="Box-sc-g0xbh4-0 MHoGG search-title">
                                                                            <a class="prc-Link-Link-85e08"
                                                                                href="/StuartIanNaylor/log2zram"><span class="Box-sc-g0xbh4-0 kzfhBO search-match prc-Text-Text-0ima0">StuartIanNaylor/log2zram</span></a>
                                                                        </div>
                                                                        <span class="Box-sc-g0xbh4-0 jkYPxx prc-Label-Label--LG6X" data-size="small" data-variant="attention">Public archive</span>
                                                                    </div>
                                                                </h3>
                                                                <div class="Box-sc-g0xbh4-0 dcdlju">
                                                                    <span class="Box-sc-g0xbh4-0 gKFdvh search-match prc-Text-Text-0ima0">Usefull for <em>IoT</em> / maker projects for reducing SD, Nand and Emmc block <em>wear</em> via log operations. Uses Zram to minimise precious memory foot…</span>
                                                                </div>
                                                                <ul class="Box-sc-g0xbh4-0 bZkODq">
                                                                    <li class="Box-sc-g0xbh4-0 iyzdzM">
                                                                        <div class="Box-sc-g0xbh4-0 hjDqIa">
                                                                            <div class="Box-sc-g0xbh4-0 gUCGVm"></div>
                                                                        </div>
                                                                        <span aria-label="Shell language">Shell</span>
                                                                    </li>
                                                                    <span class="Box-sc-g0xbh4-0 ifbKcf prc-Text-Text-0ima0" aria-hidden="true">·</span>
                                                                    <li class="Box-sc-g0xbh4-0 iyzdzM"><a
                                                                            class="Box-sc-g0xbh4-0 jJYFGF prc-Link-Link-85e08"
                                                                            href="/StuartIanNaylor/log2zram/stargazers"
                                                                            aria-label="19 stars"><svg
                                                                                aria-hidden="true" focusable="false"
                                                                                class="octicon octicon-star Octicon-sc-9kayk9-0 kPmFhj"
                                                                                viewBox="0 0 16 16" width="16"
                                                                                height="16" fill="currentColor"
                                                                                display="inline-block"
                                                                                overflow="visible"
                                                                                style="vertical-align:text-bottom">
                                                                                <path
                                                                                    d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.751.751 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Zm0 2.445L6.615 5.5a.75.75 0 0 1-.564.41l-3.097.45 2.24 2.184a.75.75 0 0 1 .216.664l-.528 3.084 2.769-1.456a.75.75 0 0 1 .698 0l2.77 1.456-.53-3.084a.75.75 0 0 1 .216-.664l2.24-2.183-3.096-.45a.75.75 0 0 1-.564-.41L8 2.694Z">
                                                                                </path>
                                                                            </svg><span class="prc-Text-Text-0ima0">19</span></a>
                                                                    </li>
                                                                    <span class="Box-sc-g0xbh4-0 ifbKcf prc-Text-Text-0ima0" aria-hidden="true">·</span>
                                                                    <li class="Box-sc-g0xbh4-0 iyzdzM">
                                                                        <span>Updated <div title="Mar 11, 2020, 1:17 AM UTC" class="Truncate__StyledTruncate-sc-23o1d2-0 liVpTx"><span class="prc-Text-Text-0ima0" title="Mar 11, 2020, 1:17 AM UTC">on Mar 11, 2020</span>
                                                            </div></span></li>
                                                            </ul>
                                                        </div>
                                                        <div class="Box-sc-g0xbh4-0 gtlRHe">
                                                            <div class="Box-sc-g0xbh4-0 fvaNTI"><a type="button"
                                                                    href="/login?return_to=https%3A%2F%2Fgithub.com%2Fsearch%3Fq%3Diot%2520wearable%26type%3Drepositories%26p%3D2"
                                                                    class="prc-Button-ButtonBase-c50BI"
                                                                    data-loading="false" data-size="small"
                                                                    data-variant="default"
                                                                    aria-describedby=":R1i8qjb:-loading-announcement"><span data-component="buttonContent" data-align="center" class="prc-Button-ButtonContent-HKbr-"><span data-component="leadingVisual" class="prc-Button-Visual-2epfX prc-Button-VisualWrap-Db-eB"><svg aria-hidden="true" focusable="false" class="octicon octicon-star" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" display="inline-block" overflow="visible" style="vertical-align:text-bottom"><path d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.751.751 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Zm0 2.445L6.615 5.5a.75.75 0 0 1-.564.41l-3.097.45 2.24 2.184a.75.75 0 0 1 .216.664l-.528 3.084 2.769-1.456a.75.75 0 0 1 .698 0l2.77 1.456-.53-3.084a.75.75 0 0 1 .216-.664l2.24-2.183-3.096-.45a.75.75 0 0 1-.564-.41L8 2.694Z"></path></svg></span><span data-component="text" class="prc-Button-Label-pTQ3x">Star</span></span></a>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                       """))  # Output: "This is a test."