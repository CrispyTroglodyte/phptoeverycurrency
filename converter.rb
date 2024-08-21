
amount_in_php = Float( ARGV[0] )
exchange_rate = Float( ARGV[1] )

converted_amount = amount_in_php * exchange_rate
puts "%.2f" % converted_amount