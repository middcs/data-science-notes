function Div (div)
  if div.classes:includes('hide') and div.classes:includes('solution') then
    return pandoc.RawBlock("markdown", "*[TODO: Your response here]*")
  else
    return nil
  end
end