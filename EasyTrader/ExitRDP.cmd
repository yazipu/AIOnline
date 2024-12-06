:: https://mrxiao.net/disconnect-rdp-keep-windows-desktop-active.html
:: https://www.joinquant.com/view/community/detail/898874c59a24051f2e2e385584f05643
for /f "skip=1 tokens=3" %%s in ('query user %USERNAME%') do (
  %windir%\System32\tscon.exe %%s /dest:console
)
:: pause